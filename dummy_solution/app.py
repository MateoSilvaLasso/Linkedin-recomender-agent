import streamlit as st
import asyncio
from dummy_solution.agente import JobOfferAgent
from dotenv import load_dotenv
import os

load_dotenv()


# Configurar la base de datos
DB_URI = os.getenv("DB_URI")
agent = JobOfferAgent(DB_URI)

# Función para ejecutar la consulta de forma asíncrona
async def get_analysis(category):
    return await agent.analyze_trends(category)

# Título de la aplicación
st.title("🔍 Análisis de Ofertas de Trabajo")

# Selector de categoría
category = st.selectbox(
    "Selecciona una categoría:",
    ["Junior", "Mid-Senior", "Senior"]
)

# Botón para obtener el análisis
if st.button("Analizar Tendencias"):
    with st.spinner("Generando análisis..."):
        response = asyncio.run(get_analysis(category))  # Ejecuta la consulta
        st.subheader("📊 Análisis del Mercado Laboral")
        st.write(response)  # Muestra el resultado en pantalla
