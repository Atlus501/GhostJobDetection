resource "aws_secretsmanager_secret" "secrets" {
  name = "ghost_job_detector/secrets"
  description = "secrets used for ghost job detector"
  tags = {
    personal_projects = "ghost_job_detector"
  }
}

resource "aws_secretsmanager_secret_version" "secrets_val" {
  secret_id     = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode(var.secrets)
}