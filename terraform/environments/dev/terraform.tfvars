# ─────────────────────────────────────────────
# Dev Environment — Cost optimised
# 1 AZ only, no flow logs
# ─────────────────────────────────────────────

environment = "dev"
project     = "platform"

# VPC
vpc_cidr = "10.0.0.0/16"

# 1 AZ only for dev — saves cost
azs = ["ap-south-1a"]

# Public subnets — one per AZ
public_subnet_cidrs = ["10.0.1.0/24"]

# Private subnets — one per AZ
private_subnet_cidrs = ["10.0.11.0/24"]

# Flow logs off in dev — not needed, saves cost
enable_flow_logs = false

tags = {
  Owner      = "dixitrit"
  CostCenter = "personal"
}