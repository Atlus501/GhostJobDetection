#creates an s3 bucket in aws
module "s3" {
    source = "./modules/s3"

    environment = "production"
    name = "tree_bucket"
    force_destroy = true
}

module secrets {
    source = "./modules/secrets"

    secrets = var.secrets
    name = "ghost_job_detector"
}

module lb {
    source = "./modules/lb"

    https = true
    lb_name = "default-lb"
    target_group_name = "application"
    target_group_port = 80
}