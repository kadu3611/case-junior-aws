import json

def handle_delete(event, usecase, criado_por):
    task_id = event["pathParameters"]["id"]

    usecase.delete_task(task_id, criado_por)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Tarefa deletada"})
    }
