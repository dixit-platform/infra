terraform {
  required_version = ">= 1.10.0"
  backend "s3" {
    bucket       = "tf-gitops-tfstate-241533123692"
    key          = "environments/prod/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}