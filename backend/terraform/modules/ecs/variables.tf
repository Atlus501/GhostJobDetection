variable ecr_name {
    type = string
    description = "the name of the ecr"
}

variable ecr_force_delete {
    type = string 
    description = "whether the ecr is force deleted"
    default = true
}

variable cluster_name{
    type = string
    description = "the name of the cluster"
}

variable task_name{
    type = string
    description = "the name of the task"
}

variable cpu {
    type = string
    description = "how much cpu is given"
    default = "1024"
}

variable memory {
    type = string
    description = "how much memory is given"
    default = "3072"
}

variable health_check_path {
    type = string
    description = "the path used for health checks"
    default = "http://localhost:80/health"
}

variable secrets_arn {
    type = string
    description = "the arn of the aws secrets manager used"
}

variable lb_listener_arn{
    type = string
    description = "the arn of the load balancer used"
}

variable lb_target_group_arn {
    type = string
    description = "arn of the lb target group"
}

variable lb_sg_id {
    type = string
    description = "the id of the load balancer security group"
}

variable container_name {
    type = string
    description = "the name of the container"
    default = "Main"
}

variable container_port {
    type = number 
    description = "the container port number"
    default = 8000
}

variable service_name {
    type = string
    description = "name of the service used"
}

variable service_desired_count {
    type = string
    description = "how many servies are desired"
    default = 1
}

variable s3_id {
    type = string
    description = "the id of the s3 bucket"
}

variable s3_arn {
    type = string
    description = "the arn of the s3 bucket"
}

variable application_security_group_name {
    type = string 
    description = "the name of the security group"
}

variable vpc_name {
    type = string
    description = "the name of the vpc"
    default = "default"
}

variable allow_s3 {
    type = bool
    description = "whether the task can access s3 buckets"
    default = true
}

variable allow_secrets {
    type = bool
    description = "whether the task can access aws secrets"
    default = true
}