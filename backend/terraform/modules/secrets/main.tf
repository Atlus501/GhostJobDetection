resource "aws_secretsmanager_secret" "secrets" {

  name = "${var.name}/secrets"
  description = "secrets used for ghost job detector"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    personal_projects = var.name
  }
}

resource "aws_secretsmanager_secret_version" "secrets_val" {

  secret_id     = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode(var.secrets)
}