from dotenv import load_dotenv
import os

from langchain_gigachat.chat_models import GigaChat

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_llm():    
    '''
    LLM initialisation
    '''
    giga = GigaChat(
        credentials=API_KEY,
        verify_ssl_certs=False,
    )

    return giga