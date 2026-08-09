variable "environment" {
    type = string
    default = "development"
}

variable "name" {
    type = string
}

variable "force_destroy" {
    type = bool
    default = false
}