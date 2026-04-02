#!/usr/bin/env python3
"""
AWS Project Management Script
Manages endpoints and EC2 instance for GitHub Actions runner
Usage: python manage_project.py --action create|destroy|start|stop
"""

import argparse
import json
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

# Load configuration
CONFIG_FILE = Path(__file__).parent / "project_config.json"


class AWSProjectManager:
    def __init__(self, config_file=CONFIG_FILE):
        """Initialize AWS clients and load configuration"""
        self.config = self._load_config(config_file)
        self.ec2_client = boto3.client("ec2", region_name=self.config["aws_region"])
        self.logger = self._setup_logger()

    @staticmethod
    def _load_config(config_file):
        """Load configuration from JSON file"""
        if not config_file.exists():
            print(f"Error: Configuration file not found at {config_file}")
            print("Please create project_config.json with your AWS resource details.")
            sys.exit(1)

        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)

    @staticmethod
    def _setup_logger():
        """Setup simple logging"""
        class Logger:
            @staticmethod
            def info(msg):
                print(f"✓ {msg}")

            @staticmethod
            def error(msg):
                print(f"✗ {msg}")

            @staticmethod
            def warning(msg):
                print(f"⚠ {msg}")

        return Logger()

    def create(self):
        """Create endpoints and start EC2"""
        print("\n" + "=" * 60)
        print("CREATING ENDPOINTS AND STARTING EC2")
        print("=" * 60)

        # Create endpoints
        print("\n[1/2] Creating endpoints...")
        for i, endpoint in enumerate(self.config["endpoints"], 1):
            self._create_endpoint(endpoint, i)

        # Start EC2
        print("\n[2/2] Starting EC2 instance...")
        self._start_ec2()

        print("\n" + "=" * 60)
        print("✓ Setup complete!")
        print("=" * 60)

    def destroy(self):
        """Stop EC2 and remove endpoints"""
        print("\n" + "=" * 60)
        print("DESTROYING ENDPOINTS AND STOPPING EC2")
        print("=" * 60)

        # Stop EC2
        print("\n[1/2] Stopping EC2 instance...")
        self._stop_ec2()

        # Delete endpoints
        print("\n[2/2] Deleting endpoints...")
        for i, endpoint in enumerate(self.config["endpoints"], 1):
            self._delete_endpoint(endpoint, i)

        print("\n" + "=" * 60)
        print("✓ Cleanup complete!")
        print("=" * 60)

    def start(self):
        """Start EC2 instance"""
        print("\n" + "=" * 60)
        print("STARTING EC2 INSTANCE")
        print("=" * 60)
        self._start_ec2()
        print("\n" + "=" * 60)
        print("✓ EC2 started!")
        print("=" * 60)

    def stop(self):
        """Stop EC2 instance"""
        print("\n" + "=" * 60)
        print("STOPPING EC2 INSTANCE")
        print("=" * 60)
        self._stop_ec2()
        print("\n" + "=" * 60)
        print("✓ EC2 stopped!")
        print("=" * 60)

    def _create_endpoint(self, endpoint, index):
        """Create a VPC Interface Endpoint"""
        try:
            # Check if endpoint already exists
            response = self.ec2_client.describe_vpc_endpoints(
                Filters=[
                    {"Name": "tag:Name", "Values": [endpoint["name"]]},
                    {"Name": "vpc-endpoint-state", "Values": ["available", "pending"]}
                ]
            )
            if response["VpcEndpoints"]:
                self.logger.warning(
                    f"Endpoint {index}: '{endpoint['name']}' already exists"
                )
                return

            # Create VPC Endpoint
            create_response = self.ec2_client.create_vpc_endpoint(
                VpcEndpointType="Interface",
                ServiceName=endpoint["service_name"],
                VpcId=self.config["vpc_id"],
                SubnetIds=endpoint["subnets"],
                SecurityGroupIds=endpoint.get("security_groups", []),
                PrivateDnsEnabled=endpoint.get("private_dns_enabled", True),
                TagSpecifications=[
                    {
                        "ResourceType": "vpc-endpoint",
                        "Tags": [{"Key": "Name", "Value": endpoint["name"]}],
                    }
                ],
            )

            endpoint_id = create_response["VpcEndpoint"]["VpcEndpointId"]
            self.logger.info(
                f"Endpoint {index}: Created '{endpoint['name']}' ({endpoint_id})"
            )

        except ClientError as e:
            self.logger.error(f"Endpoint {index}: Failed to create - {e}")

    def _delete_endpoint(self, endpoint, index):
        """Delete a VPC Interface Endpoint"""
        try:
            # Find endpoint by tag
            response = self.ec2_client.describe_vpc_endpoints(
                Filters=[
                    {"Name": "tag:Name", "Values": [endpoint["name"]]},
                    {"Name": "vpc-endpoint-state", "Values": ["available", "pending"]}
                ]
            )

            if not response["VpcEndpoints"]:
                self.logger.warning(
                    f"Endpoint {index}: '{endpoint['name']}' not found"
                )
                return

            endpoint_id = response["VpcEndpoints"][0]["VpcEndpointId"]

            # Delete endpoint
            self.ec2_client.delete_vpc_endpoints(VpcEndpointIds=[endpoint_id])
            self.logger.info(f"Endpoint {index}: Deleted '{endpoint['name']}'")

        except ClientError as e:
            self.logger.error(f"Endpoint {index}: Failed to delete - {e}")

    def _get_instance_id_from_tag(self):
        """Get EC2 instance ID by tag"""
        try:
            tag_config = self.config["ec2_tag"]
            response = self.ec2_client.describe_instances(
                Filters=[
                    {
                        "Name": f"tag:{tag_config['key']}",
                        "Values": [tag_config["value"]],
                    },
                    {"Name": "instance-state-name", "Values": ["running", "stopped"]},
                ]
            )

            if not response["Reservations"]:
                self.logger.error(
                    f"No EC2 instance found with tag '{tag_config['key']}={tag_config['value']}'"
                )
                return None

            instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]
            return instance_id

        except ClientError as e:
            self.logger.error(f"Failed to find EC2 instance: {e}")
            return None

    def _start_ec2(self):
        """Start EC2 instance"""
        instance_id = self._get_instance_id_from_tag()
        if not instance_id:
            return

        try:
            # Check current state
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            current_state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

            if current_state == "running":
                self.logger.warning(
                    f"EC2 instance '{instance_id}' is already running"
                )
                return

            # Start instance
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            self.logger.info(f"EC2 instance '{instance_id}' is starting...")

            # Wait for instance to be running
            waiter = self.ec2_client.get_waiter("instance_running")
            waiter.wait(InstanceIds=[instance_id])
            self.logger.info(f"EC2 instance '{instance_id}' is now running")

        except ClientError as e:
            self.logger.error(f"Failed to start EC2: {e}")

    def _stop_ec2(self):
        """Stop EC2 instance"""
        instance_id = self._get_instance_id_from_tag()
        if not instance_id:
            return

        try:
            # Check current state
            response = self.ec2_client.describe_instances(
                InstanceIds=[instance_id]
            )
            current_state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

            if current_state == "stopped":
                self.logger.warning(
                    f"EC2 instance '{instance_id}' is already stopped"
                )
                return

            # Stop instance
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            self.logger.info(f"EC2 instance '{instance_id}' is stopping...")

            # Wait for instance to be stopped
            waiter = self.ec2_client.get_waiter("instance_stopped")
            waiter.wait(InstanceIds=[instance_id])
            self.logger.info(f"EC2 instance '{instance_id}' is now stopped")

        except ClientError as e:
            self.logger.error(f"Failed to stop EC2: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage AWS endpoints and EC2 for GitHub Actions runner"
    )
    parser.add_argument(
        "--action",
        choices=["create", "destroy", "start", "stop"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument(
        "--config",
        default=CONFIG_FILE,
        help="Path to configuration file",
    )

    args = parser.parse_args()

    try:
        manager = AWSProjectManager(Path(args.config))
        action = getattr(manager, args.action)
        action()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
