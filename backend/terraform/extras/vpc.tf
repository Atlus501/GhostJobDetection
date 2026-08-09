data "aws_vpc" "default" {
  tags = {
    Name = vars.vpc_name
  }
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