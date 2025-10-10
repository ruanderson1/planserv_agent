from flask import Flask
from app.routes.query_route import query_bp
from app.routes.whatsapp_routes import whatsapp_bp

def create_app():
    """
    Cria e configura a aplicação Flask.
    Retorna:
        Flask: instância configurada da aplicação.
    """
    app = Flask(__name__)
    app.register_blueprint(query_bp)
    app.register_blueprint(whatsapp_bp)

    return app
