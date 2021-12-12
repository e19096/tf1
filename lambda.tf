data "archive_file" "lambda_trucks" {
  type = "zip"

  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

# resource "aws_s3_bucket_object" "lambda_trucks" {
#   bucket = aws_s3_bucket.lambda_bucket.id
#
#   key    = "lambda.zip"
#   source = data.archive_file.lambda_trucks.output_path
#
#   etag = filemd5(data.archive_file.lambda_trucks.output_path)
# }

resource "aws_lambda_function" "trucks" {
  function_name = "trucks"
  filename      = "${path.module}/lambda.zip"

  # s3_bucket = aws_s3_bucket.lambda_bucket.id
  # s3_key    = aws_s3_bucket_object.lambda_trucks.key

  runtime = "python3.9"
  handler = "trucks.handler"

  source_code_hash = data.archive_file.lambda_trucks.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
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
