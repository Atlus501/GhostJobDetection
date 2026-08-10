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

module ecs {
    source = "./modules/ecs"

    ecr_name = "ghost_job_detector"
    cluster_name = "ghost_job_detector_cluster"
    task_name = "ghost_job_detector_main_task"
    secrets_arn = module.secrets.arn
    lb_arn = module.lb.lb_arn
    service_name = "ghost_job_detecotr_service"
    s3_id = module.s3.bucket_id
    s3_arn = module.s3.bucket_arn
    application_security_group_name = "ghost_job_detector_security_group"
    lb_sg_id = module.lb.lb_sg_id
}