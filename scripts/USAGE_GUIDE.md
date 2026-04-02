# AWS Project Management Script - Commands

## Basic Usage

```bash
./manage-project.sh --action [ACTION]
```

---

## Available Actions

### `--action create`
**Purpose:** Create all 3 VPC endpoints + Start EC2 instance

**What it does:**
- Creates VPC Interface Endpoint for SSM
- Creates VPC Interface Endpoint for SSM Messages  
- Creates VPC Interface Endpoint for EC2 Messages
- Starts your GitHub Actions Runner EC2 instance
- Waits until EC2 is fully running

**When to use:** Start of your work day

**Command:**
```bash
./manage-project.sh --action create
```

---

### `--action destroy`
**Purpose:** Delete all 3 VPC endpoints + Stop EC2 instance

**What it does:**
- Deletes VPC Interface Endpoint for SSM
- Deletes VPC Interface Endpoint for SSM Messages
- Deletes VPC Interface Endpoint for EC2 Messages
- Stops EC2 instance (doesn't delete it - preserves GitHub runner)
- Waits until EC2 is fully stopped

**When to use:** End of work day (saves AWS costs)

**Command:**
```bash
./manage-project.sh --action destroy
```

---

### `--action start`
**Purpose:** Start EC2 instance ONLY (doesn't touch endpoints)

**What it does:**
- Finds EC2 by tag name
- Starts the instance
- Waits until it's running

**When to use:** 
- Endpoints already exist
- Just need to restart EC2

**Command:**
```bash
./manage-project.sh --action start
```

---

### `--action stop`
**Purpose:** Stop EC2 instance ONLY (doesn't touch endpoints)

**What it does:**
- Finds EC2 by tag name
- Stops the instance
- Waits until it's stopped

**When to use:** 
- Endpoints still needed
- Just want to pause EC2

**Command:**
```bash
./manage-project.sh --action stop
```

---

## Quick Cheat Sheet

| Command | Creates Endpoints | Starts EC2 | Deletes Endpoints | Stops EC2 |
|---------|------------------|-----------|-------------------|-----------|
| `create` | ✅ | ✅ | ❌ | ❌ |
| `destroy` | ❌ | ❌ | ✅ | ✅ |
| `start` | ❌ | ✅ | ❌ | ❌ |
| `stop` | ❌ | ❌ | ❌ | ✅ |

---

## Configuration File

Edit `project_config.json` to set:

- `aws_region` - AWS region (e.g., `ap-south-1`)
- `vpc_id` - VPC where endpoints will be created
- `ec2_tag.key` - Tag key to find EC2 (e.g., `Name`)
- `ec2_tag.value` - Tag value to match (e.g., `github-actions-runner`)
- `endpoints[].name` - Endpoint name
- `endpoints[].service_name` - AWS service (e.g., `com.amazonaws.ap-south-1.ssm`)
- `endpoints[].subnets` - Subnet IDs
- `endpoints[].security_groups` - Security group IDs
- `endpoints[].private_dns_enabled` - Enable private DNS (usually `true`)
