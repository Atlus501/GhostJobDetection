resource "aws_s3_bucket" "bucket" {
  bucket        = var.name
  force_destroy = var.force_destroy

  tags = {
    Name        = var.name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "bucket_privacy" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}