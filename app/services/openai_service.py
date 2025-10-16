from openai import OpenAI
import  time
from pymongo import MongoClient
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
load_dotenv()

# Conecta ao MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

db = client['agender_dataset']
histories_collection = db['chatHistory']

histories_collection.create_index(
    [("timestamp", 1)],
    expireAfterSeconds=1800  # 30 minutos
)
class OpenAIService:
    def __init__(self, api_key: str, number: str):
        self.client = OpenAI(api_key=api_key)
        self.history = self.get_history(number)

    def call_gpt(self, prompt: str, question: str, historico = True) -> str:
        hist = self.history
        if historico:
            hist = self.history[-3:]
        else:
            hist = ''

        messages = [{"role": "system", "content": prompt + "Historico anterior do usuário: "}] + self.history + [{"role": "user", "content": "Pergunta atual, a ser respondida: " + question}]
        print("HISTORICO: ", self.history[-3:])

        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.3,
            seed=42,
            messages=messages
        )

        response_content = response.choices[0].message.content
        response_content = response_content.replace('```', '').replace('python', '')
        return response_content

    def call_human(self, human_prompt):
        messages = [{"role": "system", "content": human_prompt}] 

        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            seed=42,
            messages=messages
        )
        human_response = response.choices[0].message.content
        return human_response
    
    def add_to_history(self, user_id, message):    
        try:
            result = histories_collection.insert_one({
                "user_id": user_id,
                "user": message,
                "timestamp": datetime.now(timezone.utc)
            })
            logging.info(f"Histórico adicionado com sucesso: {result.inserted_id}")
        except Exception as e:
            logging.error(f"Erro ao adicionar ao histórico: {e}")


    def get_history(self, user_id):
        history = list(histories_collection.find(
            {"user_id": user_id},  
            {"user": 1, "_id": 0}
        ))

        formatted_history = []
        for entry in history:
            user_text = entry.get("user", "")
            if user_text:
                formatted_history.append({"role": "user", "content": user_text})
        return formatted_history

