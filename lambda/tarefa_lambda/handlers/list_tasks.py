import json
from boto3.dynamodb.conditions import Key

def handle_list(event, table, criado_por):

    response = table.query(
        KeyConditionExpression=Key("pk").eq(f"USER#{criado_por}")
    )

    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }

