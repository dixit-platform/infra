# ─────────────────────────────────────────────
# Prod Environment — Highly available baseline
# 2 AZs, flow logs enabled
# ─────────────────────────────────────────────

environment = "prod"
project     = "platform"

# VPC
vpc_cidr = "10.2.0.0/16"

# 2 AZs for production-ready baseline
azs = ["ap-south-1a", "ap-south-1b"]

# Public subnets — one per AZ
public_subnet_cidrs = ["10.2.1.0/24", "10.2.2.0/24"]

# Private subnets — one per AZ
private_subnet_cidrs = ["10.2.11.0/24", "10.2.12.0/24"]

# Flow logs on in prod for security and auditability
enable_flow_logs         = true
flow_logs_retention_days = 90

tags = {
  Owner      = "dixitrit"
  CostCenter = "personal"
}
