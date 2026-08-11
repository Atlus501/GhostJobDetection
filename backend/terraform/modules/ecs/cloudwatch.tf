resource "aws_cloudwatch_log_group" "cw_log_group" {
  name = var.service_name
  retention_in_days = var.cw_log_retention

  tags = {
    Environment = "production"
    Service = var.service_name
    Cluster = var.cluster_name
  }
}