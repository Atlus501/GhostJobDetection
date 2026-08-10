data "aws_acm_certificate" "cert" {
    count    = var.https ? 1 : 0
    domain   = var.domain
    statuses = ["ISSUED"]
}

data "aws_vpc" "default" {
  tags = {
    Name = var.vpc_name
  }
}

data aws_subnets default {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

#security group used by the load balancer
resource "aws_security_group" "alb_sg" {
  name        = "load_balancer_security_group"
  description = "Allow HTTPS inbound traffic"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "alb_sg_in_https" {
    count = var.https ? 1 : 0
    security_group_id = aws_security_group.alb_sg.id
    cidr_ipv4         = "0.0.0.0/0"
    ip_protocol       = "tcp" # semantically equivalent to all ports
    from_port   = 443
    to_port     = 443
}

resource "aws_vpc_security_group_ingress_rule" "alb_sg_in_http" {
    security_group_id = aws_security_group.alb_sg.id
    cidr_ipv4         = "0.0.0.0/0"
    ip_protocol       = "tcp" # semantically equivalent to all ports
    from_port   = 80
    to_port     = 80
}

resource "aws_vpc_security_group_egress_rule" "alb_sb_out" {
    security_group_id = aws_security_group.alb_sg.id
    ip_protocol    = "-1"
    cidr_ipv4 = "0.0.0.0/0"
}

#the load balancers that were being created
resource "aws_lb" "alb" {
  name               = var.lb_name
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

resource "aws_lb_target_group" target_group {
    name = var.target_group_name
    port     = var.target_group_port
    protocol = "HTTP"
    vpc_id   = data.aws_vpc.default.id
    target_type = "ip"

    health_check {
      path                = var.health_check_path
      protocol            = "HTTP"
      matcher             = "200"
      interval            = 30
      timeout             = 5
      healthy_threshold   = 2
      unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" target_group {
  load_balancer_arn = aws_lb.alb.arn
  port              = var.https ? "443" : "80"
  protocol          = var.https ? "HTTPS" : "HTTP"
  ssl_policy        = var.https ? "ELBSecurityPolicy-2016-08" : null
  certificate_arn   = var.https ? data.aws_acm_certificate.cert[0].arn : null

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}

#redirects the http request
resource "aws_lb_listener" "http_redirect" {
  count             = var.https ? 1 : 0
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}