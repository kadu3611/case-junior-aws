from enum import Enum
from datetime import datetime
import uuid


class TaskStatus(Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"


class Task:

    def __init__(self, titulo, descricao, criado_por, status=TaskStatus.PENDENTE, task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.titulo = titulo
        self.descricao = descricao
        self.criado_por = criado_por
        self.status = status
        self.data_criacao = datetime.utcnow().strftime("%d/%m/%Y")
        self.data_conclusao = None

    def update_status(self, new_status: str):

        try:
            status_enum = TaskStatus[new_status]
        except KeyError:
            raise ValueError("Status aceitos: EM_ANDAMENTO e CONCLUIDO")

        self.status = status_enum

        if status_enum == TaskStatus.CONCLUIDO:
            self.data_conclusao = datetime.utcnow().strftime("%d/%m/%Y")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status.value,
            "criado_por": self.criado_por,
            "data_criacao": self.data_criacao,
            "data_conclusao": self.data_conclusao
        }