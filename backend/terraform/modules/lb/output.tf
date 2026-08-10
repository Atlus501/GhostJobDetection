output lb_arn {
    value = aws_lb.alb.arn
}

output lb_sg_id {
    value = aws_security_group.alb_sg.id
}

output target_group_arn {
    value = aws_lb_target_group.target_group.arn
}

output listener_arn{
    value = aws_lb_listener.target_group.arn
}