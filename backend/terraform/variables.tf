variable secrets {
    type = map(string)
    sensitive = true
    description = "The secrets that you are going to store. Make sure to make a file named terraform.tfvars for it"
}