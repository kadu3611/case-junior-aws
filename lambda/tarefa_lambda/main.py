import os
import boto3
from handlers.create import handle_create
from handlers.list_tasks import handle_list
from handlers.update import handle_update
from handlers.delete import handle_delete
from handlers.get_task import handle_get
from handlers.list_all_tasks import handle_all_list
from infra.task_repository import TaskRepository
from usecases.task_usecase import TaskUseCase

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
repository = TaskRepository(table)
usecase = TaskUseCase(repository)

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    path = event.get("rawPath")
    headers = event.get("headers") or {}
    criado_por = headers.get("criado_por")

    if method == "POST":
        if not criado_por:
            return {"statusCode": 400, "body": "necessário 'criado_por' no header"}
        return handle_create(event, usecase, criado_por)

    # GET /tasks/all  -> lista tudo
    if method == "GET" and path == "/tasks/all":
        return handle_all_list(table)

    # GET /tasks/{id}
    if method == "GET" and event.get("pathParameters"):
        if not criado_por:
            return {"statusCode": 400, "body": "necessário 'criado_por' no header"}
        return handle_get(event, usecase)

    # GET /tasks  -> lista por usuário
    if method == "GET" and path == "/tasks":
        if not criado_por:
            return {"statusCode": 400, "body": "necessário 'criado_por' no header"}
        return handle_list(usecase, criado_por)

    if method == "PUT":
        if not criado_por:
            return {"statusCode": 400, "body": "necessário 'criado_por' no header"}
        return handle_update(event, usecase, criado_por)

    if method == "DELETE":
        if not criado_por:
            return {"statusCode": 400, "body": "necessário 'criado_por' no header"}
        return handle_delete(event, usecase, criado_por)

    return {"statusCode": 405, "body": "Método não permitido"}
