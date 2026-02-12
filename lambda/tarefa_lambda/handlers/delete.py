import json

def handle_delete(event, table, user_id):

    task_id = event["queryStringParameters"]["task_id"]

    table.delete_item(
        Key={
            "pk": f"USER#{user_id}",
            "sk": f"TASK#{task_id}"
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Task deleted"})
    }
