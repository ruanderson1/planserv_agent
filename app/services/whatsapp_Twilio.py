from twilio.rest import Client
import os

class WhatsAppTwilio:
    def __init__(self):
        """
        Inicializa a classe com as credenciais do Twilio
        (carregadas do arquivo .env).
        """
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")  # Ex: whatsapp:+14155238886

        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError("⚠️ Variáveis TWILIO_* não configuradas corretamente no .env")

        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, para: str, mensagem: str):
        """
        Envia uma mensagem via WhatsApp usando o Twilio.
        """
        try:
            msg = self.client.messages.create(
                from_=self.from_number,
                body=mensagem,
                to=para
            )
            print(f"✅ Mensagem enviada com sucesso! SID: {msg.sid}")
            return msg.sid
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return None
