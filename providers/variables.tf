variable "region" {
  default     = "us-east-2"
  description = "AWS region"
}

variable "db_password" {
  description = "RDS root user password"
  type        = string
  sensitive   = true
}
