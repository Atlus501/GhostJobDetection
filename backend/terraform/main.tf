#creates an s3 bucket in aws
module "s3" {
    source = "./modules/s3"

    environment = "production"
    name = "boosted-tree-bucket"
    force_destroy = true
}

module secrets {
    source = "./modules/secrets"

    secrets = var.secrets
    name = "testing"
}

module lb {
    source = "./modules/lb"

    https = true
    lb_name = "default-lb"
    target_group_name = "application"
    target_group_port = 8000
}

module ecs {
    source = "./modules/ecs"

    ecr_name = "ghost_job_detector"
    cluster_name = "ghost_job_detector_cluster"
    task_name = "ghost_job_detector_main_task"
    secrets_arn = module.secrets.arn
    
    service_name = "ghost_job_detecotr_service"
    s3_id = module.s3.bucket_id
    s3_arn = module.s3.bucket_arn
    application_security_group_name = "ghost_job_detector_security_group"

    lb_listener_arn = module.lb.listener_arn
    lb_sg_id = module.lb.lb_sg_id
    lb_target_group_arn = module.lb.target_group_arn
}