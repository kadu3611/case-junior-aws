import json
import uuid

def handle_create(event, table, criado_por):
    body = json.loads(event["body"])

    task_id = str(uuid.uuid4())

    item = {
        "pk": f"USER#{criado_por}",
        "sk": f"TASK#{task_id}",
        "titulo": body["titulo"],
        "descricao": body.get("descricao", ""),
        "criado_por": criado_por
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }