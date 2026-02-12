def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    path_parameters = event.get("pathParameters") or {}
    task_id = path_parameters.get("id")
    nome_usuario = event["headers"].get("nome_usuario")

    if not nome_usuario:
        return response(400, "necessário nome_usuario no header")

    if method == "POST":
        return create_task_handler(event, nome_usuario)

    elif method == "GET" and task_id:
        return get_task_handler(nome_usuario, task_id)

    elif method == "GET":
        return list_tasks_handler(nome_usuario)

    elif method == "PUT":
        return update_task_handler(event, nome_usuario, task_id)

    elif method == "DELETE":
        return delete_task_handler(nome_usuario, task_id)

    return response(404, "Route not found")
