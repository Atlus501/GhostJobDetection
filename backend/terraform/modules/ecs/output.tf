output ecr_arn {
    value = aws_ecr_repository.ecr.arn
}

output cluster_arn {
    value = aws_ecs_cluster.cluster.arn
}

output service_id {
    value = aws_ecs_service.service.id
}

output task_arn {
    value = aws_ecs_task_definition.main_task.arn
}