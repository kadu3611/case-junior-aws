import json

def handle_update(event, table, criado_por):

    task_id = event["pathParameters"]["id"]
    body = json.loads(event["body"])

    table.update_item(
        Key={
            "pk": f"USER#{criado_por}",
            "sk": f"TASK#{task_id}"
        },
        UpdateExpression="SET titulo = :t, descricao = :d",
        ExpressionAttributeValues={
            ":t": body["titulo"],
            ":d": body.get("descricao", "")
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Tarefa Atualizada"})
    }

