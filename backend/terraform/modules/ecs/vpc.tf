data "aws_vpc" "default" {
  tags = {
    Name = var.vpc_name
  }
}

#security group used by the application
resource "aws_security_group" "application_sg" {
    name        = var.application_security_group_name
    description = "Allow HTTPS inbound traffic from alb-sg"
    vpc_id      = data.aws_vpc.default.id
} 

resource "aws_vpc_security_group_ingress_rule" "application_sg_in" {
    security_group_id = aws_security_group.application_sg.id
    referenced_security_group_id = var.lb_sg_id
    ip_protocol       = "tcp" # semantically equivalent to all ports
    from_port   = 8000
    to_port     = 8000
}

resource "aws_vpc_security_group_egress_rule" "application_sg_all_out" {
    security_group_id = aws_security_group.application_sg.id
    ip_protocol    = "-1"
    cidr_ipv4 = "0.0.0.0/0"
}