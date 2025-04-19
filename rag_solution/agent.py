from llama_index.readers.mongodb import SimpleMongoReader
from pymongo import MongoClient
import os, pymongo, pprint
from pymongo.operations import SearchIndexModel
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, ExactMatchFilter, FilterOperator
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent, FunctionAgent
from llama_index.core.workflow import Context
from llama_index.core import load_index_from_storage

class JobMongoOfferLinkedin:
    def __init__(self, uri):
        self.gemini_api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = GoogleGenAI(model="gemini-2.5-pro-exp-03-25", token=self.gemini_api_key)
        self.embed_model = GoogleGenAIEmbedding(model="gemini-embedding-exp-03-07", token=self.gemini_api_key)
        Settings.llm = self.llm 
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 100
        Settings.chunk_overlap = 10
        
        self.uri = uri
        self.mongo_client = pymongo.MongoClient(uri)
        self.atlas_vector_store = MongoDBAtlasVectorSearch(
            self.mongo_client,
            db_name = "llamaindex_db",
            collection_name = "test",
            vector_index_name = "vector_index"
        )
        self.vector_store_context = StorageContext.from_defaults(vector_store=self.atlas_vector_store)
        self.vector_store_index = VectorStoreIndex.from_vector_store(self.atlas_vector_store)
        self.vector_engine = self.vector_store_index.as_query_engine(similarity_top_k=10)
        self.query_engine_tools = [
            QueryEngineTool.from_defaults(
                query_engine=self.vector_engine,
                name="Linkedin_tool",
                description="use this tool to get information from the Linkedin database",
            )
        ]
        self.linkedin_agent = ReActAgent(
                name="Linkedin",
                description="use this agent to get information from the Linkedin database",
                tools=self.query_engine_tools,
                llm=self.llm,
                system_prompt="""
                                Eres un asistente útil con acceso a una base de datos de información extraída de perfiles de LinkedIn mediante web scraping. Tu tarea es analizar las tendencias del mercado laboral a partir de esta información y ofrecer recomendaciones valiosas para candidatos interesados en cualquier tipo de posición. Cuando el usuario te indique un área de actividad o un interés profesional, deberás generar un análisis detallado que incluya:

                                1.  **Un resumen exhaustivo de las tendencias laborales actuales** identificadas a partir de los datos de LinkedIn. Esto debe incluir las habilidades más demandadas en general, los sectores con mayor crecimiento o demanda, los tipos de roles emergentes y cualquier otra observación relevante sobre la evolución del mercado laboral. Profundiza en los factores que impulsan estas tendencias y sus implicaciones para los profesionales.

                                2.  **Recomendaciones detalladas para candidatos interesados en todas las posiciones**, independientemente de su título específico. Estas recomendaciones deben ser prácticas y aplicables, abarcando aspectos como el desarrollo de habilidades transferibles clave (comunicación, resolución de problemas, pensamiento crítico, adaptabilidad, etc.), la importancia del networking y la construcción de una marca personal sólida en LinkedIn, estrategias efectivas para la búsqueda de empleo en el entorno digital actual, y la necesidad de un aprendizaje continuo para mantenerse relevante en un mercado en constante cambio. Explica en detalle por qué cada recomendación es importante y cómo los candidatos pueden implementarla.

                                3.  **Una lista de cursos recomendados específicamente para adquirir o fortalecer las habilidades identificadas como tendencias clave en el mercado laboral.** Para cada habilidad recomendada, sugiere al menos dos cursos concretos que los candidatos podrían realizar. Indica claramente la plataforma en la que se ofrece cada curso (por ejemplo, Coursera, edX, LinkedIn Learning, Udemy, etc.). Asegúrate de que los cursos sean relevantes para el desarrollo profesional general y aplicables a diversas áreas de trabajo. Proporciona una breve descripción de lo que el candidato aprenderá en cada curso y cómo esa habilidad se relaciona con las tendencias laborales actuales.

                                El usuario te proporcionará la actividad o el interés profesional. Responde únicamente con el texto continuo del análisis y las recomendaciones, sin utilizar estructuras JSON. Extiéndete en tus explicaciones y análisis para proporcionar información valiosa y práctica.
                            """
                
        )

        self.ctx = Context(self.linkedin_agent)
        
    async def execute(self, query:str):
        handler = self.linkedin_agent.run(query, ctx=self.ctx)
        response = await handler
        return str(response)


