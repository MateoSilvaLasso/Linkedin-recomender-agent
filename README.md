# LinkedIn Data Science Job Scraper

Este proyecto realiza **web scraping** en LinkedIn para extraer ofertas de trabajo en el campo de **Data Science**, almacena la información en una base de datos y utiliza un **agente de IA** para proporcionar recomendaciones sobre cómo mejorar las probabilidades de conseguir un empleo en este campo.

## Tecnologías Utilizadas 🛠️

- **Selenium**: Para la automatización del navegador y extracción de datos.
- **LlamaIndex**: Para organizar y estructurar la información extraída y crear el agente.
- **Gemini 2.0 API**: Para generar recomendaciones sobre cómo mejorar el perfil y conseguir un empleo.
- **Streamlit**: Para la interfaz de usuario interactiva.
- **Base de datos postgres en supabase**: Para almacenar y consultar las ofertas de trabajo extraídas.

## Instalación 🚀

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate    # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar credenciales
Crea un archivo `.env` en la raíz del proyecto con las credenciales necesarias:
```env
GOOGLE_API_KEY = api key of your agent
#The next three options are used if you need to be your own web scraping, the scheme that i used is this CREATE TABLE ofertas_linkedin (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), titulo TEXT NOT NULL #descripcion JSONB NOT NULL,categoria TEXT NOT NULL);
SUPABASE_URL = url of your data base
SUPABASE_KEY = key of of you data base
MY_PASSWORD = your linkedin password

DB_URI = the uri of your data base
```

## Uso 🔥

### 1. Ejecutar el scraper
```bash
python scraper.py
```
Este comando iniciará el proceso de scraping en LinkedIn y almacenará los datos en la base de datos configurada.

### 2. Iniciar la interfaz de usuario con Streamlit
```bash
streamlit run app.py
```
Esto abrirá una interfaz gráfica donde podrás ver las ofertas de trabajo extraídas y obtener recomendaciones sobre cómo mejorar tu perfil para aplicar a estos trabajos.

## Funcionalidades ✨

- **Scraping de LinkedIn**: Extrae ofertas de empleo para Data Science de LinkedIn.
- **Almacenamiento en base de datos**: Guarda los datos extraídos para futuras consultas.
- **Interfaz de usuario con Streamlit**: Permite visualizar las ofertas y recibir recomendaciones.
- **Recomendaciones con IA**: Utiliza la API de Gemini 2.0 para sugerencias personalizadas sobre cómo mejorar tu perfil profesional.

## Posibles Mejoras 🚀

- Integrar notificaciones automáticas para nuevas ofertas de trabajo.
- Mejorar la estrategia de scraping para evitar bloqueos por parte de LinkedIn.

## Contribución 🤝
Si quieres contribuir a este proyecto, ¡eres bienvenido! Puedes hacer un **fork**, crear una nueva rama y enviar un **pull request**.

---

💡 *Desarrollado por Mateo Silva.*

