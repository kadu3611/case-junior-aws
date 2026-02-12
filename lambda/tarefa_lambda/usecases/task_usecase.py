from domain.task import Task


class TaskUseCase:

    def __init__(self, repository):
        self.repository = repository

    def create_task(self, data, criado_por):
        task = Task(
            titulo=data["titulo"],
            descricao=data["descricao"],
            status=data.get("status", "Pendente"),
            criado_por=criado_por
            )
        
        self.repository.create(task)

        return task.to_response()

    def get_task(self, task_id):
        item = self.repository.get_by_id(task_id)

        if not item:
            return None

        task = Task(
            titulo=item["titulo"],
            descricao=item["descricao"],
            status=item.get("status", "Pendente"),
            criado_por=item["criado_por"],
            task_id=item["id"],
            data_criacao=item["data_criacao"],
            data_conclusao=item.get("data_conclusao")
        )

        return task.to_response()

    def list_tasks(self, criado_por):
        items = self.repository.get_all()

        tasks = []

        for item in items:
            task = Task(
                titulo=item["titulo"],
                descricao=item["descricao"],
                status=item.get("status", "Pendente"),
                criado_por=criado_por,
                task_id=item["id"],
                data_criacao=item["data_criacao"],
                data_conclusao=item.get("data_conclusao")
            )
            tasks.append(task.to_response())

        return tasks

    def update_task(self, task_id, data, criado_por):
        existing = self.repository.get_by_id(task_id)
        self.repository.update(
            task_id,
            titulo = data.get("titulo", existing.get("titulo")),
            descricao = data.get("descricao", existing.get("descricao")),
            status= existing.get("status", "Pendente"),
            data_conclusao = data.get("data_conclusao", existing.get("data_conclusao")),
            criado_por = criado_por
        )

    def delete_task(self, task_id, criado_por):
        self.repository.delete(task_id)
            # ,
            # ConditionExpression="criado_por = :cp",
            # ExpressionAttributeValues={
            #     ":cp": criado_por
            # }
        
