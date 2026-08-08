# -----------------------------------------------------------------------------
# 1. ECS TASK ROLE (Used by your FastAPI application at runtime)
# -----------------------------------------------------------------------------

resource "aws_iam_role" "ecs_task_role" {
  name = "task_role"

  # Trust policy allowing ECS tasks to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# Attach S3 read permissions to the Task Role
resource "aws_iam_role_policy" "task_role_s3_policy" {
  name = "task_role_s3_policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        # Bucket ARN + object wildcard ARN
        Resource = [
          aws_s3_bucket.tree_bucket.arn,
          "${aws_s3_bucket.tree_bucket.arn}/*"
        ]
      }
    ]
  })
}

# -----------------------------------------------------------------------------
# 2. ECS EXECUTION ROLE (Used by the ECS Agent to pull images & fetch secrets)
# -----------------------------------------------------------------------------

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "task_execution_role"

  # Trust policy allowing ECS to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# Standard AWS Managed Policy for pulling from ECR and pushing CloudWatch logs
resource "aws_iam_role_policy_attachment" "ecs_execution_standard" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Custom policy allowing the ECS agent to retrieve values from Secrets Manager
resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "ecs_execution_secrets_policy"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.secrets.arn
        ]
      }
    ]
  })
}