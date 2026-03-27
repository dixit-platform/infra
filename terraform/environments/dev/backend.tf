terraform {
  backend "s3" {
    bucket       = "tf-gitops-tfstate-241533123692"
    key          = "environments/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}