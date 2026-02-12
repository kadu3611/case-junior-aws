import json

def handle_get_by_id(event, table, user_id):

    task_id = event["pathParameters"]["id"]

    response = table.get_item(
        Key={
            "pk": f"USER#{user_id}",
            "sk": f"TASK#{task_id}"
        }
    )

    item = response.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Tarefa não existe"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }