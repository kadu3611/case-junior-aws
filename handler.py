def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    path_parameters = event.get("pathParameters") or {}
    task_id = path_parameters.get("id")
    criado_por = event["headers"].get("criado_por")

    if not criado_por:
        return response(400, "necessário criado_por no header")

    if method == "POST":
        return create_task_handler(event, criado_por)

    elif method == "GET" and task_id:
        return get_task_handler(criado_por, task_id)

    elif method == "GET":
        return list_tasks_handler(criado_por)

    elif method == "PUT":
        return update_task_handler(event, criado_por, task_id)

    elif method == "DELETE":
        return delete_task_handler(criado_por, task_id)

    return response(404, "Route not found")
