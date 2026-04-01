output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = module.vpc.vpc_cidr
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = module.vpc.internet_gateway_id
}

output "public_subnet_ids" {
  description = "Map of AZ to public subnet ID"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Map of AZ to private subnet ID"
  value       = module.vpc.private_subnet_ids
}

output "public_route_table_id" {
  description = "ID of the public route table"
  value       = module.vpc.public_route_table_id
}

output "private_route_table_id" {
  description = "ID of the private route table"
  value       = module.vpc.private_route_table_id
}
