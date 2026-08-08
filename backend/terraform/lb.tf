resource "aws_lb" "alb" {
  name               = "ghost-job-detector-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

data "aws_acm_certificate" "cert" {
    domain   = "helloworld-portfolio-projects.click"
    statuses = ["ISSUED"]
}

resource "aws_lb_target_group" "ghost_job_detector" {
    name = "ghost_job_detector"
    port     = 80
    protocol = "HTTP"
    vpc_id   = aws_vpc.default.id
}

resource "aws_lb_listener" "ghost_job_detector" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ghost_job_detector.arn
  }
}