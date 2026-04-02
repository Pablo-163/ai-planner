from dotenv import load_dotenv
import os
import re

import json
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

def invoke_text(prompt: str) -> str:
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content.strip()

def invoke_json(prompt: str) -> dict:
    '''
    Парсинг ответка в json. Перед загрузкой проводится очистка от Markdown мусора
    '''
    llm = get_llm()
    response = llm.invoke(prompt)
    raw_text = response.content.strip()

    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract JSON block from response: {raw_text}")

    json_text = match.group(1)
    return json.loads(json_text)