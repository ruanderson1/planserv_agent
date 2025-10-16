from flask import Blueprint, request, jsonify
from app.services.whatsapp_Twilio import WhatsAppTwilio
from app.services.lead_service import LeadService

whatsapp_bp = Blueprint("whatsapp", __name__)
whatsapp = WhatsAppTwilio()

@whatsapp_bp.route("/whatsapp/webhook", methods=["POST"])
def whatsapp_webhook():
    """
     Endpoint webhook responsável por receber mensagens do WhatsApp enviadas via Twilio, 
     processá-las e responder automaticamente ao remetente.

     A função extrai o número do remetente e o conteúdo da mensagem da requisição POST 
     enviada pelo Twilio, delega o processamento ao LeadService e envia a resposta 
     gerada de volta ao usuário por meio do serviço whatsApp_Twilio.
    """
    incoming_data = request.form
    sender = incoming_data.get("From")  
    message = incoming_data.get("Body")  

    print(f"Mensagem recebida de {sender}: {message}")

    lead_service = LeadService(sender)
    
    reply = lead_service.process_message(message)
    # ------------- descomentar quando for para whatsapp, nao so pra teste--------------------------------------------------------
    # whatsapp.send_message(sender, reply) 
    return jsonify({"status": "ok", "message": reply}), 200
