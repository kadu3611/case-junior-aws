class CreateTaskDTO:
    def __init__(self, titulo: str, descricao: str, criado_por: str):
        if not titulo:
            raise ValueError("Necessário o parametro de texto 'titulo'")

        if not criado_por:
            raise ValueError("Necessário o parametro de texto 'criado_por'")

        self.titulo = titulo
        self.descricao = descricao or ""
        self.criado_por = criado_por

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            titulo=data.get("titulo"),
            descricao=data.get("descricao"),
            criado_por=data.get("criado_por"),
        )
