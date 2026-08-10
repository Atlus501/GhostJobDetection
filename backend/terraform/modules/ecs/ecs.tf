# Fetch public subnets in default VPC
data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  tags = {
    type = "public"
  }
}

#1. create the ecr that stores the image
resource "aws_ecr_repository" "ecr" {
  name                 = var.ecr_name
  image_tag_mutability = "MUTABLE"
  force_delete = var.ecr_force_delete
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = true
  }
}

#2. create the cluster that serves the services
resource "aws_ecs_cluster" "cluster" {
  name = var.cluster_name

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "main_task" {
  family                   = var.task_name
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  network_mode             = "awsvpc"

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name      = var.container_name
      image     = "${aws_ecr_repository.ecr.repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
          appProtocol   = "http"
        }
      ]

      environment = [
        { name = "GLM_MODEL", value = "glm-4.7-flash" },
        { name = "PINECONE_INDEX_NAME", value = "ghostjobs" },
        { name = "PINECONE_NAMESPACE", value = "jobs" },
        { name = "HOST", value = "0.0.0.0" },
        { name = "PORT", value = "80" },
        { name = "LOGGER_FILE", value = "ghostdetection.log" },
        { name = "ENVIRONMENT", value = "production" }
      ]

      secrets = [
        {
          name      = "APP_SECRETS"
          valueFrom = var.secrets_arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.task_name}"
          "awslogs-create-group"  = "true"
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      # Fixed Health Check (Curling HTTP port 80 locally inside container)
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f ${var.health_check_path} || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
}

resource "aws_ecs_service" "service" {
    name = var.service_name
    cluster = aws_ecs_cluster.cluster.id
    task_definition=aws_ecs_task_definition.main_task.arn
    desired_count = var.service_desired_count
    availability_zone_rebalancing = "ENABLED"
    scheduling_strategy = "REPLICA"

    capacity_provider_strategy {
      base = 0
      weight = 1
      capacity_provider = "FARGATE"
    }

    load_balancer {
        target_group_arn = var.lb_target_group_arn
        container_name   = var.container_name
        container_port   = var.container_port
    }

    network_configuration {
        subnets          = data.aws_subnets.public.ids
        security_groups  = [aws_security_group.application_sg.id]
        assign_public_ip = true
    }

    depends_on = [var.lb_listener_arn]
}