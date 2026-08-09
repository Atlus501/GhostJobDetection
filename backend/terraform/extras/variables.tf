variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "secrets" {
  description = "secrets that must be stored in aws secrets manager"
  sensitive = true
  type = map(string)
}

variable "user_arn" {
  description = "arn of the user"
  sensitive = true
  type = string
}