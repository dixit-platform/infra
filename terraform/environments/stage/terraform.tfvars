# ─────────────────────────────────────────────
# Stage Environment — Production-like
# 2 AZs, flow logs enabled
# ─────────────────────────────────────────────

environment = "stage"
project     = "platform"

# VPC
vpc_cidr = "10.1.0.0/16"

# 2 AZs for better parity with production
azs = ["ap-south-1a", "ap-south-1b"]

# Public subnets — one per AZ
public_subnet_cidrs = ["10.1.1.0/24", "10.1.2.0/24"]

# Private subnets — one per AZ
private_subnet_cidrs = ["10.1.11.0/24", "10.1.12.0/24"]

# Flow logs on in stage for observability practice
enable_flow_logs = false

tags = {
  Owner      = "dixitrit"
  CostCenter = "personal"
}
