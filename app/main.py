"""
Módulo principal da aplicação Flask.
Inicializa o app e importa as dependências.
"""

from app import create_app
from app.utils.db import get_db

app = create_app()
db = get_db()  # Conexão com o MongoDB

# Exposição para o Flask CLI, testes e execução via run.py
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
