data "archive_file" "lambda_trucks" {
  type = "zip"

  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "trucks" {
  function_name    = "trucks"
  filename         = "${path.module}/lambda.zip"
  runtime          = "python3.6"
  handler          = "trucks.handler"
  source_code_hash = data.archive_file.lambda_trucks.output_base64sha256
  role             = aws_iam_role.lambda_exec.arn
  layers = [
    "arn:aws:lambda:us-east-2:898466741470:layer:psycopg2-py36:1",
  ]
  environment {
    variables = {
      DB_HOST     = aws_db_instance.z3l.address,
      DB_NAME     = aws_db_instance.z3l.name,
      DB_PORT     = aws_db_instance.z3l.port,
      DB_USER     = aws_db_instance.z3l.username,
      DB_PASSWORD = var.db_password,
    }
  }
}

resource "aws_cloudwatch_log_group" "trucks" {
  name = "/aws/lambda/${aws_lambda_function.trucks.function_name}"

  retention_in_days = 30
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
