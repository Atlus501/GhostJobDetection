module secrets {
    source = "./modules/secrets"

    secrets = var.secrets
    name = "ghost_job_detector"
}