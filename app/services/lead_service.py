"""
Serviço responsável por gerenciar conversas, armazenar leads e gerar respostas.
"""

from app.utils.db import get_db
from app.models.lead_model import Lead

class LeadService:
    """
    Classe que gerencia o fluxo de conversas e o armazenamento de leads no MongoDB.
    """

    def __init__(self):
        self.db = get_db()
        self.collection = self.db["leads"]

    def get_lead(self, number):
        """
        Recupera um lead existente pelo número do WhatsApp.
        Caso não exista, cria um novo lead.

        Args:
            number (str): Número do usuário no WhatsApp.

        Retorna:
            dict: Documento do lead.
        """
        lead = self.collection.find_one({"number": number})
        if not lead:
            new_lead = Lead(number)
            self.collection.insert_one(new_lead.to_dict())
            return new_lead.to_dict()
        return lead

    def update_lead(self, number, updates):
        """
        Atualiza informações de um lead existente no banco.

        Args:
            number (str): Número do usuário.
            updates (dict): Campos a serem atualizados.
        """
        self.collection.update_one({"number": number}, {"$set": updates})

    def process_message(self, number, message):
        """
        Processa a mensagem recebida do usuário e define a próxima resposta.

        Args:
            number (str): Número do usuário.
            message (str): Texto recebido via WhatsApp.

        Retorna:
            str: Resposta apropriada para o estágio atual.
        """
        lead = self.get_lead(number)
        stage = lead.get("stage", "ask_name")

        if stage == "ask_name":
            self.update_lead(number, {"name": message.strip(), "stage": "ask_service"})
            return f"Prazer, {message}! 😊 Qual tipo de serviço você deseja?"

        elif stage == "ask_service":
            self.update_lead(number, {"service": message.strip(), "stage": "ask_time"})
            return "Perfeito! Qual seria o melhor horário pra você?"

        elif stage == "ask_time":
            self.update_lead(number, {"time": message.strip(), "stage": "ask_phone"})
            return "Certo! E qual seu telefone para contato?"

        elif stage == "ask_phone":
            self.update_lead(number, {"phone": message.strip(), "stage": "done"})
            lead = self.get_lead(number)
            return (
                f"Obrigado, {lead['name']}! 🙌\n"
                f"🧾 Serviço: {lead['service']}\n"
                f"🕐 Horário: {lead['time']}\n"
                f"📞 Telefone: {lead['phone']}\n\n"
                "Em breve entraremos em contato para confirmar. 😊"
            )

        elif stage == "done":
            self.update_lead(number, {"stage": "ask_service"})
            return (
                f"Oi {lead.get('name', 'amigo(a)')}! Quer fazer outro agendamento? "
                "Me diga o tipo de serviço. 💬"
            )

        else:
            self.update_lead(number, {"stage": "ask_name"})
            return "Olá! 😊 Como posso te chamar?"
