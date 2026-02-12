import json

def handle_create(event, usecase, criado_por):
    body = json.loads(event["body"])
    result = usecase.create_task(body, criado_por)
    print("BODY:", event["body"])
    return {
        "statusCode": 201,
        "body": json.dumps(result)
    }
