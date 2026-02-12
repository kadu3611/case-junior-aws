data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/tarefa_lambda/main.py"
  output_path = "${path.module}/tarefa_lambda.zip"
}

resource "aws_lambda_function" "tarefa" {
  function_name = "tarefa-crud"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.10"
  handler       = "main.lambda_handler"
  timeout       = 15

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = "Tarefa"
    }
  }
}
