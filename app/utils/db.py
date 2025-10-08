"""
Módulo de conexão com o MongoDB.
Responsável por criar e retornar a conexão com o banco de dados.
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """
    Cria e retorna a instância do banco de dados MongoDB.
    
    Retorna:
        db (Database): Objeto de conexão com o banco de dados definido no .env.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["planserv_db"]
    return db
