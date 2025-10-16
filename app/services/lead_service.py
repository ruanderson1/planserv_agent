"""
Serviço responsável por gerenciar conversas, armazenar leads e gerar respostas.
"""

from datetime import datetime
from app.utils.db import get_db
from app.models.lead_model import Lead
from app.services.whatsapp_Twilio import WhatsAppTwilio
from app.services.openai_service import OpenAIService
from app.services.prompts_service import Prompts_service
import os
class LeadService:
    """
    Classe que gerencia o fluxo de conversas e o armazenamento de leads no MongoDB.
    """

    def __init__(self, number):
        self.db = get_db()
        self.collection = self.db["leads"]
        self.whatsapp = WhatsAppTwilio()  # 🔹 Inicializa o serviço Twilio
        self.openai = OpenAIService(os.getenv("OPENAI_API_KEY"), number)  # 🔹 Inicializa o serviço OpenAI
        self.prompts_service = Prompts_service(self.openai, number)  # 🔹 Inicializa o serviço de prompts
        self.number = number 

    # def get_lead(self):
    #     """
    #     Recupera um lead existente pelo número do WhatsApp.
    #     Caso não exista, cria um novo lead.
    #     """
    #     lead = self.collection.find_one({"number": self.number})
    #     if not lead:
    #         new_lead = Lead(self.number)
    #         self.collection.insert_one(new_lead.to_dict())
    #         return new_lead.to_dict()
    # #     return lead

    # def update_lead(self, updates):
    #     """Atualiza informações de um lead existente no banco."""
    #     self.collection.update_one({"number": self.number}, {"$set": updates})

    # def process_message(self, self.number, message):
    #     """
    #     Processa a mensagem recebida e envia a resposta via WhatsApp.
    #     """
    #     lead = self.get_lead(self.number)
    #     stage = lead.get("stage", "ask_name")

    #     if stage == "ask_name":
    #         self.update_lead(self.number, {"name": message.strip(), "stage": "ask_service"})
    #         resposta = f"Prazer, {message}! 😊 Qual tipo de serviço você deseja?"

    #     elif stage == "ask_service":
    #         self.update_lead(self.number, {"service": message.strip(), "stage": "ask_time"})
    #         resposta = "Perfeito! Qual seria o melhor horário pra você?"

    #     elif stage == "ask_time":
    #         self.update_lead(self.number, {"time": message.strip(), "stage": "ask_phone"})
    #         resposta = "Certo! E qual seu telefone para contato?"

    #     elif stage == "ask_phone":
    #         self.update_lead(self.number, {"phone": message.strip(), "stage": "done"})
    #         lead = self.get_lead(self.number)
    #         resposta = (
    #             f"Obrigado, {lead['name']}! 🙌\n"
    #             f"🧾 Serviço: {lead['service']}\n"
    #             f"🕐 Horário: {lead['time']}\n"
    #             f"📞 Telefone: {lead['phone']}\n\n"
    #             "Em breve entraremos em contato para confirmar. 😊"
    #         )

    #     elif stage == "done":
    #         self.update_lead(self.number, {"stage": "ask_service"})
    #         resposta = (
    #             f"Oi {lead.get('name', 'amigo(a)')}! Quer fazer outro agendamento? "
    #             "Me diga o tipo de serviço. 💬"
    #         )

    #     else:
    #         self.update_lead(self.number, {"stage": "ask_name"})
    #         resposta = "Olá! 😊 Para iniciarmos poderia me dizer seu nome?"

    #     # Envia a resposta via Twilio WhatsApp
    #     # self.whatsapp.enviar_mensagem(self.number, resposta)

    #     return resposta


    def process_message(self, message):
        """
        Processa a mensagem recebida via WhatsApp, gera uma resposta usando a OpenAI
        e armazena ou atualiza as informações do lead no banco de dados.

        Args:
            message (str): Conteúdo da mensagem enviada pelo usuário.

        Returns:
            str: Resposta gerada pela IA e enviada de volta ao usuário.
        """

        # Verifica se o lead já existe no banco
        existing_lead = self.collection.find_one({"number": self.number})

        #  Se não existir, cria um novo registro de lead
        if not existing_lead:
            new_lead = Lead(number=self.number, stage="start")
            lead_data = new_lead.to_dict()
            lead_data["source"] = "whatsapp"
            self.collection.insert_one(lead_data)
            print(f"[INFO] Novo lead criado: {self.number}")

        # Gera a resposta via OpenAI
        try:
            response = self.prompts_service.generate_response(message)
        except Exception as e:
            print(f"[ERRO] Falha ao gerar resposta: {e}")
            response = "Desculpe, houve um erro ao processar sua mensagem. Tente novamente mais tarde."

        # Atualiza o registro do lead com a última mensagem e data
        self.collection.update_one(
            {"number": self.number},
            {
                "$set": {
                    "last_message": message,
                    "last_response": response,
                    "last_interaction": datetime.now(),
                    "source": "whatsapp"
                }
            },
        )

        # 5. Envia a resposta via WhatsApp
        self.whatsapp.send_message(self.number, response)

        print(f"[INFO] Resposta enviada para {self.number}: {response}")

        return response
























        # lead = self.get_lead(number)
        # stage = lead.get("stage", "ask_name")

        # if stage == "ask_name":
        #     self.update_lead(number, {"name": message.strip(), "stage": "ask_service"})
        #     resposta = f"Prazer, {message}! 😊 Qual tipo de serviço você deseja?"

        # elif stage == "ask_service":
        #     self.update_lead(number, {"service": message.strip(), "stage": "ask_time"})
        #     resposta = "Perfeito! Qual seria o melhor horário pra você?"

        # elif stage == "ask_time":
        #     self.update_lead(number, {"time": message.strip(), "stage": "ask_phone"})
        #     resposta = "Certo! E qual seu telefone para contato?"

        # elif stage == "ask_phone":
        #     self.update_lead(number, {"phone": message.strip(), "stage": "done"})
        #     lead = self.get_lead(number)
        #     resposta = (
        #         f"Obrigado, {lead['name']}! 🙌\n"
        #         f"🧾 Serviço: {lead['service']}\n"
        #         f"🕐 Horário: {lead['time']}\n"
        #         f"📞 Telefone: {lead['phone']}\n\n"
        #         "Em breve entraremos em contato para confirmar. 😊"
        #     )

        # elif stage == "done":
        #     self.update_lead(number, {"stage": "ask_service"})
        #     resposta = (
        #         f"Oi {lead.get('name', 'amigo(a)')}! Quer fazer outro agendamento? "
        #         "Me diga o tipo de serviço. 💬"
        #     )

        # else:
        #     self.update_lead(number, {"stage": "ask_name"})
        #     resposta = "Olá! 😊 Para iniciarmos poderia me dizer seu nome?"

        # # Envia a resposta via Twilio WhatsApp
        # # self.whatsapp.enviar_mensagem(number, resposta)

        # return resposta
