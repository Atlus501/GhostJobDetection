resource "aws_s3_bucket" "tree_bucket" {
  bucket        = "ghost-job-detector-information"
  force_destroy = true

  tags = {
    Name        = "ghost-job-detector-models"
    Environment = var.environment
    Model       = "gradient_boosted_tree"
  }
}

resource "aws_s3_bucket_public_access_block" "tree_bucket_privacy" {
  bucket = aws_s3_bucket.tree_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tree_bucket_encryption" {
  bucket = aws_s3_bucket.tree_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}