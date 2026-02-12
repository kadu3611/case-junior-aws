import json
from boto3.dynamodb.conditions import Key

def handle_all_list(table):

    response = table.scan()

    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }

