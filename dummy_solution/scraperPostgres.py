from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import uuid
import json  # Para convertir la descripción en JSON
from supabase import create_client, Client
from dotenv import load_dotenv
import os

class LinkedInScraper:
    def __init__(self, email, password, supabase_url, supabase_key):
        self.email = email
        self.password = password
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.driver = None  # Se inicializará al iniciar sesión
        
        # Lista de URLs con categorías
        self.urls = [
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=1%2C2", "Junior"),
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=3%2C4", "Mid-Senior"),
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=5%2C6", "Senior")
        ]

    def iniciar_sesion(self):
        """Inicia sesión en LinkedIn."""
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)  # Esperar la carga de la página

    def extraer_ofertas(self, max_paginas=3):
        """Extrae ofertas de empleo y navega por las páginas usando aria-label."""
        datos = []

        for url, categoria in self.urls:
            self.driver.get(url)
            time.sleep(5)  # Esperar carga inicial

            for pagina in range(1, max_paginas + 1):  # Páginas a recorrer
                time.sleep(5)  # Esperar carga de la página

                ofertas = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'UgAtFMnqZqqxuTjIJqVIvqbSfpzZgfNYY')]/li")

                for oferta in ofertas:
                    oferta.click()
                    time.sleep(2)

                    try:
                        titulo = self.driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text
                        descripcion = self.driver.find_element(By.CLASS_NAME, "jobs-description-content__text--stretch").text
                    except:
                        continue  # Saltar si no encuentra datos

                    descripcion_json = json.dumps({"texto": descripcion})
                    if any(word in titulo.lower() for word in ["Data science", "IA", "datos", "data", "AI", "Analista","Analitica", "Analitycs"]):
                        print(f"La oferta tiene que ver con AI {titulo}")
                        datos.append({
                            "id": str(uuid.uuid4()),  
                            "titulo": titulo,
                            "descripcion": descripcion_json,
                            "categoria": categoria
                        })

                # Hacer clic en el botón de la siguiente página basado en `aria-label`
                siguiente_pagina = pagina + 1
                try:
                    boton_siguiente = self.driver.find_element(By.XPATH, f"//button[@aria-label='Page {siguiente_pagina}']")
                    self.driver.execute_script("arguments[0].click();", boton_siguiente)
                    time.sleep(5)  # Esperar la nueva página
                except:
                    print(f"No se encontró el botón para la página {siguiente_pagina}. Terminando paginación.")
                    break  # Si no hay botón para la siguiente página, detenerse

        return datos

    def guardar_en_supabase(self, datos):
        """Guarda las ofertas extraídas en Supabase."""
        if datos:
            response = self.supabase.table("ofertas_linkedin").insert(datos).execute()
            print("Datos guardados en Supabase:", response)

    def cerrar(self):
        """Cierra el navegador."""
        if self.driver:
            self.driver.quit()

    def ejecutar_scraper(self, ofertas_por_pagina= 5):
        """Ejecuta todo el proceso de scraping y almacenamiento."""
        self.iniciar_sesion()
        datos = self.extraer_ofertas(max_paginas=ofertas_por_pagina)
        self.guardar_en_supabase(datos)
        self.cerrar()


if __name__ == "__main__":
    load_dotenv()
    EMAIL = "mateosilva1901@gmail.com"
    PASSWORD = os.getenv("MY_PASSWORD")  # ⚠️ Usa variables de entorno en producción
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    scraper = LinkedInScraper(EMAIL, PASSWORD, SUPABASE_URL, SUPABASE_KEY)
    scraper.ejecutar_scraper(ofertas_por_pagina=5)  