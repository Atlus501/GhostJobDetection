variable https {
    type = bool
    description = "Whether the load balancer is http or https based"
}

variable vpc_name {
    type = string
    description = "The name of the vpc network you are going to use"
    default = "default"
}

variable lb_name {
    type = string
    description = "The name of the load balancer"
}

variable domain {
    type = string
    description = "The domain of the ssl certificate"
    default = "helloworld-portfolio-projects.click"
}

variable target_group_name {
    type = string
    description = "The name of the load balancer target group"
}

variable target_group_port {
    type = number
    description = "The port for the container"
}

variable health_check_path {
    type = string
    description = "The path used for health checks"
    default = "/health"
}