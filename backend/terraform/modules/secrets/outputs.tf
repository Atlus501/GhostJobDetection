output id {
    value = aws_secretsmanager_secret.secrets.id
    description = "The id of the secrets manager"
}

output arn {
    value = aws_secretsmanager_secret.secrets.arn
    description = "The arn of the secrets manager"
}