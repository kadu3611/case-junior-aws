import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Tarefa")


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]

    user_id = event["headers"].get("criado_por")

    if not user_id:
        return response(400, {"message": "Necessário o parametro 'criado_por' no Header"})

    # CREATE
    if method == "POST" and path == "/tasks":
        body = json.loads(event["body"])

        task_id = str(uuid.uuid4())

        item = {
            "pk": f"USER#{user_id}",
            "sk": f"TASK#{task_id}",
            "id": task_id,
            "titulo": body["titulo"],
            "descricao": body.get("descricao", ""),
            "status": "PENDENTE",
            "criado_por": user_id,
            "data_criacao": datetime.utcnow().strftime("%Y-%m-%d"),
            "data_conclusao": None
        }

        table.put_item(Item=item)

        return response(201, item)

    return response(404, {"message": "Route not found"})
