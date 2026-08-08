resource "aws_ecr_repository" "backend_repository" {
  name                 = "ghost-job-detector-backend"
  image_tag_mutability = "MUTABLE"
  force_delete = true
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = true
  }
}