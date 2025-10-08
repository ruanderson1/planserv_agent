"""
Rota principal do agente.
Recebe mensagens do servidor Node.js e responde conforme o fluxo.
"""

from flask import Blueprint, request, jsonify
from app.services.lead_service import LeadService

query_bp = Blueprint("query", __name__)
lead_service = LeadService()

@query_bp.route("/query", methods=["POST"])
def handle_query():
    """
    Endpoint para processar mensagens recebidas via WhatsApp.

    Corpo esperado:
        {
            "question": "Mensagem do usuário",
            "number": "Número do WhatsApp"
        }

    Retorna:
        JSON: { "message": "Resposta do bot" }
    """
    data = request.get_json()
    message = data.get("question")
    number = data.get("number")

    if not message or not number:
        return jsonify({"message": "Dados inválidos."}), 400

    response = lead_service.process_message(number, message)
    return jsonify({"message": response})
