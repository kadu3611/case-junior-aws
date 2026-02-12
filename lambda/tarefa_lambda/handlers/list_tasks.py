import json

def handle_list(usecase, criado_por):
    tasks = usecase.list_tasks(criado_por)

    return {
        "statusCode": 200,
        "body": json.dumps(tasks)
    }
