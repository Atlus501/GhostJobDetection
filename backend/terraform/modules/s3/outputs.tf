output "bucket_id" {
    description = "This is the bucket id"
    value = aws_s3_bucket.bucket.id
}

output "bucket_arn" {
    description = "This is the bucket arn"
    value = aws_s3_bucket.bucket.arn
}

output "bucket_domain_name" {
  description = "The bucket domain name."
  value       = aws_s3_bucket.bucket.bucket_domain_name
}