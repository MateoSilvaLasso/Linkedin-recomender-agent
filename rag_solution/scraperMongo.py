
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import uuid
from datetime import datetime
from mongoengine import connect, Document, StringField, DateTimeField
from dotenv import load_dotenv
import os

# Definición del modelo (como lo tienes)
class Linkedin(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(required=True)
    category = StringField(required=False)
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'datos_linkedin',
        'indexes': [
            'title',
            {'fields': ['description'], 'unique': True}
        ]
    }

class LinkedInScraperMongoEngine:
    def __init__(self, email, password, mongo_uri):
        self.email = email
        self.password = password
        
        # Conexión con MongoEngine
        connect(host=mongo_uri, alias='default')
        
        self.driver = None
        
        # URLs de búsqueda
        self.urls = [
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=1%2C2", "Junior"),
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=3%2C4", "Mid-Senior"),
            ("https://www.linkedin.com/jobs/search/?keywords=data%20science&f_E=5%2C6", "Senior")
        ]

    def iniciar_sesion(self):
        """Inicia sesión en LinkedIn con opciones para evitar detección."""
        #options = webdriver.ChromeOptions()
        #options.add_argument("--start-maximized")
        #options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome()#options=options)
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        self.driver.find_element(By.ID, "username").send_keys(self.email)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

    def extraer_ofertas(self, max_paginas=3):
        """Extrae ofertas respetando el esquema definido."""
        ofertas_procesadas = 0
        
        for url, categoria in self.urls:
            self.driver.get(url)
            time.sleep(5)

            for pagina in range(1, max_paginas + 1):
                time.sleep(3)
                
                # Selector actualizado para 2024
                ofertas = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'scaffold-layout__list-item')]")
                
                for oferta in ofertas:
                    try:
                        oferta.click()
                        time.sleep(2)
                        
                        # Extracción de datos
                        titulo = self.driver.find_element(
                            By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title"
                        ).text.strip()
                        
                        descripcion = self.driver.find_element(
                            By.CLASS_NAME, "jobs-description-content__text--stretch"
                        ).text.strip()
                        
                        # Verificar si es relevante
                        if not self._es_relevante(titulo, descripcion):
                            continue
                        
                        # Crear documento con MongoEngine
                        try:
                            Linkedin(
                                title=titulo,
                                description=descripcion,
                                category=categoria
                            ).save()  # MongoEngine maneja el created_at automáticamente
                            
                            ofertas_procesadas += 1
                            print(f"✅ Oferta guardada: {titulo[:50]}...")
                            
                        except Exception as db_error:
                            print(f"⚠️ Error al guardar (puede ser duplicado): {str(db_error)}")
                            
                    except Exception as e:
                        print(f"Error procesando oferta: {str(e)}")
                        continue
                
                # Paginación
                try:
                    self._avanzar_pagina(pagina + 1)
                except:
                    break
        
        return ofertas_procesadas

    def _es_relevante(self, titulo, descripcion):
        """Filtra ofertas relevantes."""
        palabras_clave = [
            "data science", "ia", "datos", "data", 
            "ai", "analista", "analitica", "machine learning",
            "ml", "data engineer", "ciencia de datos"
        ]
        titulo_lower = titulo.lower()
        desc_lower = descripcion.lower()
        
        return any(palabra in titulo_lower or palabra in desc_lower 
                  for palabra in palabras_clave)

    def _avanzar_pagina(self, numero_pagina):
        """Maneja la paginación con reintentos."""
        intentos = 0
        while intentos < 3:
            try:
                boton = self.driver.find_element(
                    By.XPATH, f"//button[@aria-label='Page {numero_pagina}']"
                )
                self.driver.execute_script("arguments[0].click();", boton)
                time.sleep(5)
                return True
            except:
                intentos += 1
                time.sleep(2)
        return False

    def generar_estadisticas(self):
        """Genera métricas usando agregaciones de MongoEngine."""
        from mongoengine.queryset.visitor import Q
        
        total = Linkedin.objects.count()
        por_categoria = Linkedin.objects.aggregate([
            {"$group": {
                "_id": "$category",
                "count": {"$sum": 1},
                "latest": {"$max": "$created_at"}
            }}
        ])
        
        print("\n📊 Estadísticas de Ofertas:")
        print(f"Total ofertas almacenadas: {total}")
        print("Por categoría:")
        for cat in por_categoria:
            print(f"- {cat['_id']}: {cat['count']} (última: {cat['latest'].strftime('%Y-%m-%d')}")

    def cerrar(self):
        """Cierra recursos."""
        if self.driver:
            self.driver.quit()

    def ejecutar(self, paginas=3):
        """Flujo completo de ejecución."""
        try:
            self.iniciar_sesion()
            total = self.extraer_ofertas(max_paginas=paginas)
            print(f"\n🎉 Proceso completado. {total} ofertas procesadas.")
            self.generar_estadisticas()
        except Exception as e:
            print(f"❌ Error durante la ejecución: {str(e)}")
        finally:
            self.cerrar()


if __name__ == "__main__":
    load_dotenv()
    
    # Configuración desde variables de entorno
    CONFIG = {
        "email": "mateosilva1901@gmail.com",
        "password": os.getenv("MY_PASSWORD"),
        "mongo_uri": f"mongodb+srv://MateoSilva19:{os.getenv('MONGO_PASSWORD')}@cluster0.febcypy.mongodb.net/Linkedin?retryWrites=true&w=majority&appName=Cluster0"
    }
    
    # Validar configuración
    if not all(CONFIG.values()):
        raise ValueError("Faltan variables de entorno en el archivo .env")
    
    # Ejecutar scraper
    scraper = LinkedInScraperMongoEngine(
        email=CONFIG["email"],
        password=CONFIG["password"],
        mongo_uri=CONFIG["mongo_uri"]
    )
    
    scraper.ejecutar(paginas=3)