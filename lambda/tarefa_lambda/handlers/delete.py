import json

def handle_delete(event, table, user_id):

    task_id = event["pathParameters"]["id"]

    table.delete_item(
        Key={
            "pk": f"USER#{user_id}",
            "sk": f"TASK#{task_id}"
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Tarefa deletada"})
    }
