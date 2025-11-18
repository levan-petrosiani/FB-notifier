from langchain_ollama import ChatOllama
from config import SYSTEM_PROMPT

llm = ChatOllama(model="llama3.2", temperature=0)

def is_offer_post(text: str) -> bool:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    response = llm.invoke(messages).content.strip().upper()
    return response == "YES"
