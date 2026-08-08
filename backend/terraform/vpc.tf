data "aws_vpc" "default" {
  default = true
}

#security group used by the load balancer
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Allow HTTPS inbound traffic"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_vpc_security_group_ingress_rule" "alb_sg_in_https" {
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

#security group used by the application
resource "aws_security_group" "application_sg" {
    name        = "application_sg"
    description = "Allow HTTPS inbound traffic from alb-sg"
    vpc_id      = data.aws_vpc.default.id
} 

resource "aws_vpc_security_group_ingress_rule" "application_sg_in" {
    security_group_id = aws_security_group.application_sg.id
    referenced_security_group_id = aws_security_group.alb_sg.id
    ip_protocol       = "tcp" # semantically equivalent to all ports
    from_port   = 80
    to_port     = 80
}

resource "aws_vpc_security_group_egress_rule" "application_sg_all_out" {
    security_group_id = aws_security_group.application_sg.id
    ip_protocol    = "-1"
    cidr_ipv4 = "0.0.0.0/0"
}