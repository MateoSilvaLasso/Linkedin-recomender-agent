# 🔍 LinkedIn Data Science Job Scraper

Este repositorio contiene **dos versiones** de un proyecto que realiza scraping en **LinkedIn** para extraer ofertas de empleo en el campo de **Data Science**, con capacidades de recomendación basadas en modelos de lenguaje (LLMs).

---

## 📁 Estructura del Proyecto

```
.
├── dummy_solution/       → Versión básica del proyecto (Streamlit + PostgreSQL)
├── rag_solution/    → Versión robusta con RAG, MongoDB, embeddings y Streamlit
├── requirements.txt
|── .env
└── README.md
```

---

## 🧪 Versión 1 — Dummy (`v1_dummy/`)

Una versión inicial y funcional que:
- Realiza scraping con **Selenium**
- Almacena los datos en **PostgreSQL (Supabase)**
- Utiliza **Gemini 2.0 API** para generar recomendaciones
- Manda el **texto completo** de las ofertas como contexto en cada prompt

> ❗ Esto puede ser **costoso y poco eficiente** en uso de tokens, especialmente si se quiere escalar o trabajar con muchos datos.

---

## 🚀 Versión 2 — Avanzada con RAG (`v2_advanced/`)

Una solución más potente y optimizada que:
- Realiza scraping con **Selenium**
- Almacena los datos estructurados en **MongoDB**
- Genera **embeddings semánticos** de cada oferta
- Utiliza **RAG (Retrieval-Augmented Generation)** para enviar al LLM solo la información más relevante, no todo el corpus
- Escala mucho mejor en volumen y complejidad de consultas

---

## ⚖️ Comparación: Dummy vs RAG

| Característica                    | Dummy (`v1_dummy`)                            | RAG (`v2_advanced`)                             |
|----------------------------------|-----------------------------------------------|-------------------------------------------------|
| Modelo de recuperación           | Prompt completo                                | Búsqueda semántica con embeddings               |
| Costo por token                  | Alto (todo el texto va al LLM)                | Bajo (solo se manda lo relevante)              |
| Escalabilidad                    | Limitada                                       | Alta, por separación de almacenamiento y consulta |
| Precisión en recomendaciones     | Genérica (basada en texto bruto)              | Contextual (basada en similitud semántica)      |
| Almacenamiento                   | Relacional (PostgreSQL)                        | NoSQL + vectores (MongoDB + vector store)       |
| Ideal para                       | Prototipado rápido                             | Producción o sistemas más robustos              |

> ✅ **Ventaja clave de la versión con RAG**:  
> **Reduce el uso de tokens**, lo que disminuye los costos por consulta y mejora la calidad de las respuestas al enfocarse solo en la información relevante.

---

## 🛠 Tecnologías Utilizadas

- **Selenium**
- **Streamlit**
- **LlamaIndex**
- **Gemini 2.0 API**
- **PostgreSQL (v1) / MongoDB + vector store (v2)**

---

## Instalación

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
Crea un archivo .env en la raíz del proyecto con las credenciales necesarias:
```env
GOOGLE_API_KEY = api key of your agent
#The next three options are used if you need to be your own web scraping, the scheme that i used is this CREATE TABLE ofertas_linkedin (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), titulo TEXT NOT NULL #descripcion JSONB NOT NULL,categoria TEXT NOT NULL);
SUPABASE_URL = url of your data base
SUPABASE_KEY = key of of you data base
MY_PASSWORD = your linkedin password
COMPLETED_PASSWORD = your completed uri(with password, mongo)
DB_URI = the uri of your data base(postgress)
```

## 🧪 ¿Cómo probar cada versión?

### Versión Dummy
```bash
cd dummy_solution
streamlit run app.py
```

### Versión Avanzada (RAG)
```bash
cd rag_solution
python scraper.py       # Extrae ofertas, caso que no los tengas
streamlit run app.py  
```

para esta solucion ya los embeddings estan generados y almacenados, si quieres conocer como esta hecho, no dudes en contactarme.

---

## 🤝 Contribución

¡Eres bienvenido a contribuir! Explora cualquiera de las dos versiones, sugiere mejoras o propón nuevas funcionalidades.

---

💡 *Desarrollado por Mateo Silva — Explorando cómo los LLMs y el RAG pueden potenciar soluciones inteligentes y eficientes para la búsqueda de empleo en Data Science.*
