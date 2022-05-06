# resource "aws_apigatewayv2_api" "lambda" {
#   name          = "serverless_lambda_gw"
#   protocol_type = "HTTP"
#
#   cors_configuration {
#     allow_origins     = ["http://localhost:3000", "https://e19096.github.io"]
#     allow_credentials = "true"
#     allow_headers     = ["Content-Type", "Authorization"]
#     allow_methods     = ["GET", "OPTIONS", "POST"]
#   }
# }
#
# resource "aws_apigatewayv2_stage" "lambda" {
#   api_id = aws_apigatewayv2_api.lambda.id
#
#   name        = "serverless_lambda_stage"
#   auto_deploy = true
#
#   access_log_settings {
#     destination_arn = aws_cloudwatch_log_group.api_gw.arn
#
#     format = jsonencode({
#       requestId               = "$context.requestId"
#       sourceIp                = "$context.identity.sourceIp"
#       requestTime             = "$context.requestTime"
#       protocol                = "$context.protocol"
#       httpMethod              = "$context.httpMethod"
#       resourcePath            = "$context.resourcePath"
#       routeKey                = "$context.routeKey"
#       status                  = "$context.status"
#       responseLength          = "$context.responseLength"
#       integrationErrorMessage = "$context.integrationErrorMessage"
#       }
#     )
#   }
# }
#
# resource "aws_apigatewayv2_integration" "trucks" {
#   api_id = aws_apigatewayv2_api.lambda.id
#
#   integration_uri    = aws_lambda_function.trucks.invoke_arn
#   integration_type   = "AWS_PROXY"
#   integration_method = "POST"
# }
#
# resource "aws_apigatewayv2_route" "get_trucks" {
#   api_id    = aws_apigatewayv2_api.lambda.id
#   route_key = "GET /trucks"
#   target    = "integrations/${aws_apigatewayv2_integration.trucks.id}"
# }
#
# resource "aws_apigatewayv2_route" "options_reservations" {
#   api_id    = aws_apigatewayv2_api.lambda.id
#   route_key = "OPTIONS /reservations"
# }
#
# resource "aws_apigatewayv2_route" "get_reservations" {
#   api_id             = aws_apigatewayv2_api.lambda.id
#   route_key          = "GET /reservations"
#   target             = "integrations/${aws_apigatewayv2_integration.trucks.id}"
#   authorization_type = "JWT"
#   authorizer_id      = aws_apigatewayv2_authorizer.auth.id
# }
#
# resource "aws_apigatewayv2_route" "post_reservations" {
#   api_id             = aws_apigatewayv2_api.lambda.id
#   route_key          = "POST /reservations"
#   target             = "integrations/${aws_apigatewayv2_integration.trucks.id}"
#   authorization_type = "JWT"
#   authorizer_id      = aws_apigatewayv2_authorizer.auth.id
# }
#
# resource "aws_cloudwatch_log_group" "api_gw" {
#   name              = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"
#   retention_in_days = 30
# }
#
# resource "aws_lambda_permission" "api_gw" {
#   statement_id  = "AllowExecutionFromAPIGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.trucks.function_name
#   principal     = "apigateway.amazonaws.com"
#   source_arn    = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
# }
#
# resource "aws_apigatewayv2_authorizer" "auth" {
#   api_id           = aws_apigatewayv2_api.lambda.id
#   authorizer_type  = "JWT"
#   identity_sources = ["$request.header.Authorization"]
#   name             = "cognito-authorizer"
#
#   jwt_configuration {
#     audience = [aws_cognito_user_pool_client.client.id]
#     issuer   = "https://${aws_cognito_user_pool.pool.endpoint}"
#   }
# }
