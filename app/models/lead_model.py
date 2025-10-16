"""
Modelo de dados para representar leads e estágios de conversa.
"""

from datetime import datetime

class Lead:
    """
    Representa um lead captado via WhatsApp.

    Atributos:
        number (str): Número do usuário no WhatsApp.
        name (str): Nome do lead.
        service (str): Tipo de serviço solicitado.
        time (str): Horário desejado.
        phone (str): Telefone para contato.
        stage (str): Etapa atual da conversa.
        source (str): Fonte de onde o lead foi captado.
        created_at (datetime): Data/hora da criação do registro.
    """

    def __init__(self, number, name=None, service=None, time=None, phone=None, stage="start", source=""):
        self.number = number
        self.name = name
        self.service = service
        self.time = time
        self.phone = phone
        self.stage = stage
        self.source = source
        self.created_at = datetime.now()

    def to_dict(self):
        """Converte o objeto Lead em dicionário para inserção no MongoDB."""
        return {
            "number": self.number,
            "name": self.name,
            "service": self.service,
            "time": self.time,
            "phone": self.phone,
            "stage": self.stage,
            "source": self.source,
            "created_at": self.created_at
        }
