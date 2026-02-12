import json

def handle_get(event, usecase):
    task_id = event["pathParameters"]["id"]

    task = usecase.get_task(task_id)

    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Tarefa não encontrada"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(task)
    }
