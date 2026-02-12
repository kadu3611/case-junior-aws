import uuid
from datetime import datetime


class Task:

    STATUS_VALIDOS = ["Pendente", "Em Andamento", "Concluída"]
    
    def __init__(
        self,
        titulo,
        descricao,
        criado_por,
        status="Pendente",
        task_id=None,
        data_criacao=None,
        data_conclusao=None
    ):
        if status not in self.STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido. Permitidos: {', '.join(self.STATUS_VALIDOS)}"
            )
        self.id = task_id or str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.criado_por = criado_por
        self.data_criacao = data_criacao or datetime.utcnow().isoformat()
        self.data_conclusao = data_conclusao

    def format_date(self, date_iso):
        if not date_iso:
            return None

        date_obj = datetime.fromisoformat(date_iso)
        return date_obj.strftime("%d/%m/%Y")

    def to_dict(self):
        return {
            "pk": "TASK",
            "sk": f"TASK#{self.id}",
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "criado_por": self.criado_por,
            "data_criacao": self.data_criacao,
            "data_conclusao": self.data_conclusao
        }

    def to_response(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "criado_por": self.criado_por,
            "data_criacao": self.format_date(self.data_criacao),
            "data_conclusao": self.format_date(self.data_conclusao)
        }
