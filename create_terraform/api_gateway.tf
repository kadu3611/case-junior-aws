resource "aws_apigatewayv2_api" "tarefa_api" {
  name          = "tarefa-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = ["content-type", "criado_por"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_origins = ["*"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.tarefa_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.tarefa_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.tarefa.invoke_arn

  payload_format_version = "2.0"
}


#Criação de rotas na API
resource "aws_apigatewayv2_route" "create_task" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "POST /tasks"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "list_tasks" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "GET /tasks"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "list_all_tasks" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "GET /tasks/all"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "get_task" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "GET /tasks/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "update_task" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "PUT /tasks/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_task" {
  api_id    = aws_apigatewayv2_api.tarefa_api.id
  route_key = "DELETE /tasks/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Permisão para o lambda
resource "aws_lambda_permission" "allow_apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.tarefa.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.tarefa_api.execution_arn}/*/*"
}

#Para mostrar o endpoint
output "api_url" {
  value = aws_apigatewayv2_api.tarefa_api.api_endpoint
}