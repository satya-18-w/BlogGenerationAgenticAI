import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq



class GroqLm:
    def __init__(self):
        load_dotenv()
        
    def get_llm(self):
        try:
            os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
            llm=ChatGroq(model="qwen-2.5-32b",temperature=0.75,max_tokens=2000)
            return llm
        except Exception as e:
            raise ValueError(f"Error Occured with exception as {e}")    
