import os
import boto3
from handlers.create import handle_create
from handlers.list_tasks import handle_list
from handlers.update import handle_update
from handlers.delete import handle_delete

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]
    criado_por = event["headers"].get("criado_por")

    if not criado_por:
        return {"statusCode": 400, "body": "necessário 'criado_por' no header"}

    if method == "POST":
        return handle_create(event, table, criado_por)

    if method == "GET":
        return handle_list(event, table, criado_por)

    if method == "PUT":
        return handle_update(event, table, criado_por)

    if method == "DELETE":
        return handle_delete(event, table, criado_por)

    return {"statusCode": 405, "body": "Método não permitido"}
