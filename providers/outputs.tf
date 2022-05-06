# output "function_name" {
#   description = "Name of the Lambda function."
#
#   value = aws_lambda_function.trucks.function_name
# }
#
# output "base_url" {
#   description = "Base URL for API Gateway stage."
#
#   value = aws_apigatewayv2_stage.lambda.invoke_url
# }
#
# output "rds_hostname" {
#   description = "RDS instance hostname"
#   value       = aws_db_instance.z3l.address
#   sensitive   = true
# }
#
# output "rds_port" {
#   description = "RDS instance port"
#   value       = aws_db_instance.z3l.port
#   sensitive   = true
# }
#
# output "rds_username" {
#   description = "RDS instance root username"
#   value       = aws_db_instance.z3l.username
#   sensitive   = true
# }
