from flask import Blueprint, request, jsonify
from app.services.whatsapp_Twilio import WhatsAppTwilio
from app.services.lead_service import LeadService

whatsapp_bp = Blueprint("whatsapp", __name__)
whatsapp = WhatsAppTwilio()
lead_service = LeadService()

@whatsapp_bp.route("/whatsapp/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_data = request.form
    sender = incoming_data.get("From")  
    message = incoming_data.get("Body")  

    print(f"Mensagem recebida de {sender}: {message}")

    reply = lead_service.process_message(sender, message)
    whatsapp.send_message(sender, reply)

    return jsonify({"status": "ok", "message": reply}), 200
