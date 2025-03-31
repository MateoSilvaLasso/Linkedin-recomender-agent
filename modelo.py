from llama_index.readers.database import DatabaseReader
from sqlalchemy import create_engine
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from dotenv import load_dotenv

class JobOfferAgent:
    def __init__(self, db_uri):
        load_dotenv()
        self.engine = create_engine(db_uri, connect_args={"options": "-c client_encoding=utf8"})
        self.reader = DatabaseReader(engine=self.engine)
        self.llm = GoogleGenAI(model="gemini-2.0-flash")
        self.consult_agent = ReActAgent(
            name="consult work agent",
            description="Is able to give you information about the job offers.",
            system_prompt="""
                Lo que te llega son ofertas de trabajo extraídas de una base de datos. 
                Escribe un análisis detallado sobre las tendencias en el mercado laboral y 
                recomendaciones para candidatos interesados en todas las posiciones en general sin importar el título. 
                Solo dame el texto con que recomiendas, ademas recomienda que cursos hacer para adquirir esas hablidades. Responde solo con texto continuo, sin estructurar en JSON 
                ni agregar etiquetas como 'Thought' o 'Action'.
            """,
            llm=self.llm,
        )
        self.workflow = AgentWorkflow(
            agents=[self.consult_agent],
            root_agent="consult work agent"
        )

    async def analyze_trends(self, category):
        query = f"""
        SELECT titulo, descripcion, categoria
        FROM ofertas_linkedin
        WHERE categoria = '{category}';
        """
        
        documents = self.reader.load_data(query=query)
        job_offers = "\n".join([doc.text for doc in documents])
        
        response = await self.consult_agent.run(user_msg=job_offers)
        return str(response)
