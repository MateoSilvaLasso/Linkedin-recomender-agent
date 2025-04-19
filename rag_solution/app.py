import streamlit as st
import asyncio
from agent import JobMongoOfferLinkedin
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("COMPLETED_PASSWORD")
agent = JobMongoOfferLinkedin(uri)

async def get_analysis(category):
    return await agent.execute(category)

st.title("🔍 Análisis de Ofertas de Trabajo en la IA")

st.text_input("Introduce a que tipo de trabajo deseas aplicar", key="category_input")

if st.button("Analizar Tendencias"):
    with st.spinner("Generando análisis..."):
        response = asyncio.run(get_analysis(st.session_state.category_input))
        st.subheader("📊 Análisis del Mercado Laboral")
        st.write(response)  # Muestra el resultado en pantalla
