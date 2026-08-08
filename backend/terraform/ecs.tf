data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_ecs_cluster" "ghost_job_detector_cluster" {
  name = "ghost_job_detector"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "main_task" {
    family                   = "ghost_job_detection"
    requires_compatibilities = ["FARGATE"]
    cpu = "1024"
    memory = "3072"
    
    execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
    task_role_arn      = aws_iam_role.ecs_task_role.arn
    network_mode = "awsvpc"
    

    container_definitions = jsonencode([{
        "name" : "Main",
        "image": "893410593768.dkr.ecr.us-east-1.amazonaws.com/personal_project/ghost_job_detector@sha256:43c01f257b5c3bf871b38dbd3f9c811591b06b8650378744e53a854e6dba3b71",
        "cpu": 0,
        "portMappings": [
            {
                "containerPort": 80,
                "hostPort": 80,
                "protocol": "tcp",
                "name": "80",
                "appProtocol": "http"
            }
        ],
        "environment" : [
            {
                "name": "GLM_MODEL",
                "value": "glm-4.7-flash"
            },
            {
                "name": "PINECONE_INDEX_NAME",
                "value": "ghostjobs"
            },
             {
                "name": "PINECONE_NAMESPACE",
                "value": "jobs"
            },
            {
                "name": "HOST",
                "value": "0.0.0.0"
            },
            {
                "name": "PORT",
                "value": "80"
            },
            {
                "name": "LOGGER_FILE",
                "value": "ghostdetection.log"
            },
            {
                "name": "ENVIRONMENT",
                "value" : "production"
            }
        ],
        "secrets": [
            {
                "name": "APP_SECRETS",
                "valueFrom": aws_secretsmanager_secret.secrets.arn
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/ecs/ghost_job_detection",
                "awslogs-create-group": "true",
                "awslogs-region": "us-east-1",
                "awslogs-stream-prefix": "ecs"
            },
            "secretOptions": []
        },
        "healthCheck": {
            "command": [
                "CMD-SHELL",
                "curl -f http://localhost:443/health || exit 1"
            ],
            "interval": 30,
            "timeout": 5,
            "retries": 3,
            "startPeriod" : 60
        },
    }])
}

resource "aws_ecs_service" "ghost_job_detection_service" {
    name = "ghost_job_detector"
    cluster = aws_ecs_cluster.ghost_job_detector_cluster.id
    task_definition=aws_ecs_task_definition.main_task.arn
    desired_count = 1
    availability_zone_rebalancing = "ENABLED"
    scheduling_strategy = "REPLICA"

    capacity_provider_strategy {
      base = 0
      weight = 1
      capacity_provider = "FARGATE"
    }

    load_balancer {
        target_group_arn = aws_lb_target_group.ghost_job_detector.arn
        container_name   = "Main"
        container_port   = 80
    }

    network_configuration {
        subnets          = data.aws_subnets.default.ids
        security_groups  = [aws_security_group.application_sg.id]
        assign_public_ip = false
    }

    depends_on = [aws_lb_listener.ghost_job_detector]
}