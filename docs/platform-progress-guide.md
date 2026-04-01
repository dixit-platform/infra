# DevSecOps GitOps Platform

Complete Setup and Progress Guide  
AWS · Terraform · GitHub Actions · DevSecOps · Platform Engineering

## Steps Completed

Steps 1-11 completed from the existing setup baseline.

## Resume From

Step 12: First VPC module

## End Goal

Build a production-grade, multi-environment AWS platform using Terraform and GitHub Actions, then evolve it into an internal developer platform with reusable modules, secure delivery workflows, and self-service infrastructure patterns.

Version 1.0  
Last updated: April 1, 2026

## Project Vision

This project is the hands-on learning track for DevOps, Platform Engineering, and DevSecOps tooling across AWS and GitHub. The short-term goal is to build production-quality infrastructure modules and delivery pipelines. The long-term goal is to turn those building blocks into an internal platform that developers can safely consume through repeatable workflows.

## Roadmap

| Step | Status | What it covers |
|------|--------|----------------|
| Step 1-11 | Done | Security baseline, IAM, runner, bootstrap, CI/CD, promote, destroy |
| Step 12 | In progress | Reusable Terraform VPC module wired into dev, stage, and prod |
| Step 13 | Next | Import the existing runner VPC into Terraform state |
| Step 14 | Planned | EC2 and ALB reusable modules |
| Step 15 | Planned | ECS reusable module |
| Step 16 | Planned | Migrate runner from EC2 to ECS Fargate |
| Step 17 | Planned | EKS reusable module |
| Step 18 | Planned | Migrate runner to EKS with ARC |
| Step 19 | Planned | Internal developer portal |

## Current State Snapshot

### Repository

- Infra repo contains reusable Terraform environments for `dev`, `stage`, and `prod`.
- GitHub Actions workflows already exist for CI, promotion, and destroy flows.
- A reusable VPC module exists at `terraform/modules/vpc`.

### Current Implementation State

- `dev`, `stage`, and `prod` environment entrypoints now target the shared VPC module.
- `dev` remains cost-optimized with one AZ and flow logs disabled.
- `stage` and `prod` now have explicit VPC inputs with two AZs and flow logs enabled.
- Environment outputs now expose core VPC values for later modules and validations.

## Locked-In Decisions

- AWS region stays `ap-south-1`.
- Terraform stays on `>= 1.10.0` with S3 native locking.
- No DynamoDB table for state locking.
- No static AWS access keys.
- No NAT Gateway in this learning platform.
- Dev uses a low-cost baseline.
- Stage and prod keep stronger observability defaults through VPC Flow Logs.
- Reusable Terraform modules remain the main delivery pattern.

## Current Step

### Step 12: First VPC Module

**Goal**  
Replace the starter S3 demo resources in each Terraform environment with the reusable VPC module and establish environment-specific inputs for dev, stage, and prod.

**Files changed**  
- `terraform/environments/dev/main.tf`
- `terraform/environments/dev/outputs.tf`
- `terraform/environments/stage/main.tf`
- `terraform/environments/stage/variables.tf`
- `terraform/environments/stage/terraform.tfvars`
- `terraform/environments/stage/outputs.tf`
- `terraform/environments/prod/main.tf`
- `terraform/environments/prod/variables.tf`
- `terraform/environments/prod/terraform.tfvars`
- `terraform/environments/prod/outputs.tf`

**Terraform inputs chosen**  
- Dev VPC CIDR: `10.0.0.0/16`
- Stage VPC CIDR: `10.1.0.0/16`
- Prod VPC CIDR: `10.2.0.0/16`
- Dev AZ count: 1
- Stage AZ count: 2
- Prod AZ count: 2
- Flow logs: disabled in dev, enabled in stage and prod
- NAT Gateway: not used

**Validation performed**  
- `terraform fmt -check -recursive terraform` passed.
- Environment wrappers standardized around the shared `module "vpc"` interface.
- Environment outputs aligned to the shared module outputs.
- Verified there are no remaining `aws_s3_bucket`, `random_id`, or demo bucket references in the environment entrypoints.
- Full `terraform init`, `validate`, and `plan` are still pending on a machine or runner with AWS credentials and access to `registry.terraform.io`.

**Learnings**  
- The reusable module was already present, but the environment entrypoints were still pointing to temporary demo resources.
- Stage and prod configuration files needed to be completed before environment-level validation could be meaningful.
- Exposing shared outputs early will make later ECS, ALB, and EKS modules easier to connect.

**Next step**  
Run `terraform init`, `terraform validate`, and `terraform plan` for `dev`, `stage`, and `prod` from the GitHub runner or any machine that has AWS credentials plus Terraform registry access, then move to Step 13 import work.

## Working Notes

Use this section as the ongoing change log for the project:

| Date | Step | Update |
|------|------|--------|
| 2026-04-01 | Step 12 | Replaced environment demo resources with the shared VPC module and created environment-specific tfvars for dev, stage, and prod. |
| 2026-04-01 | Step 12 | Confirmed formatting passed locally and documented that backend/provider validation must run from a credentialed environment with Terraform registry access. |
