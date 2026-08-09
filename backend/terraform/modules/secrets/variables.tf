variable "secrets" {
    type = map(string)
    sensitive = true
    description = "The secrets that you'd like to store"
}

variable name {
    type = string
    description = "The name of the secrets manager"
}