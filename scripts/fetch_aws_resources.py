#!/usr/bin/env python3
"""
AWS Resource Discovery Script
Fetches VPCs, Subnets, Security Groups, and EC2 instances
to help populate project_config.json
"""

import json
import boto3
from botocore.exceptions import ClientError


class AWSResourceFetcher:
    def __init__(self, region="ap-south-1"):
        """Initialize AWS clients"""
        self.region = region
        self.ec2_client = boto3.client("ec2", region_name=region)
        self.elbv2_client = boto3.client("elbv2", region_name=region)

    def fetch_vpcs(self):
        """Fetch all VPCs"""
        try:
            response = self.ec2_client.describe_vpcs()
            vpcs = []
            for vpc in response["Vpcs"]:
                vpc_data = {
                    "VpcId": vpc["VpcId"],
                    "CidrBlock": vpc["CidrBlock"],
                    "Tags": {tag["Key"]: tag["Value"] for tag in vpc.get("Tags", [])},
                }
                vpcs.append(vpc_data)
            return vpcs
        except ClientError as e:
            print(f"Error fetching VPCs: {e}")
            return []

    def fetch_subnets(self, vpc_id=None):
        """Fetch all subnets (optionally filtered by VPC)"""
        try:
            filters = []
            if vpc_id:
                filters.append({"Name": "vpc-id", "Values": [vpc_id]})

            response = self.ec2_client.describe_subnets(Filters=filters)
            subnets = []
            for subnet in response["Subnets"]:
                subnet_data = {
                    "SubnetId": subnet["SubnetId"],
                    "VpcId": subnet["VpcId"],
                    "CidrBlock": subnet["CidrBlock"],
                    "AvailabilityZone": subnet["AvailabilityZone"],
                    "Tags": {tag["Key"]: tag["Value"] for tag in subnet.get("Tags", [])},
                }
                subnets.append(subnet_data)
            return subnets
        except ClientError as e:
            print(f"Error fetching Subnets: {e}")
            return []

    def fetch_security_groups(self, vpc_id=None):
        """Fetch all security groups (optionally filtered by VPC)"""
        try:
            filters = []
            if vpc_id:
                filters.append({"Name": "vpc-id", "Values": [vpc_id]})

            response = self.ec2_client.describe_security_groups(Filters=filters)
            sgs = []
            for sg in response["SecurityGroups"]:
                sg_data = {
                    "GroupId": sg["GroupId"],
                    "GroupName": sg["GroupName"],
                    "VpcId": sg["VpcId"],
                    "Description": sg["Description"],
                    "Tags": {tag["Key"]: tag["Value"] for tag in sg.get("Tags", [])},
                }
                sgs.append(sg_data)
            return sgs
        except ClientError as e:
            print(f"Error fetching Security Groups: {e}")
            return []

    def fetch_ec2_instances(self):
        """Fetch all EC2 instances with their details"""
        try:
            response = self.ec2_client.describe_instances(
                Filters=[
                    {"Name": "instance-state-name", "Values": ["running", "stopped"]}
                ]
            )
            instances = []
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_data = {
                        "InstanceId": instance["InstanceId"],
                        "InstanceType": instance["InstanceType"],
                        "State": instance["State"]["Name"],
                        "PrivateIpAddress": instance.get("PrivateIpAddress"),
                        "PublicIpAddress": instance.get("PublicIpAddress"),
                        "VpcId": instance.get("VpcId"),
                        "SubnetId": instance.get("SubnetId"),
                        "SecurityGroups": [
                            sg["GroupId"] for sg in instance.get("SecurityGroups", [])
                        ],
                        "Tags": {
                            tag["Key"]: tag["Value"]
                            for tag in instance.get("Tags", [])
                        },
                    }
                    instances.append(instance_data)
            return instances
        except ClientError as e:
            print(f"Error fetching EC2 instances: {e}")
            return []

    def fetch_load_balancers(self):
        """Fetch all existing ALBs"""
        try:
            response = self.elbv2_client.describe_load_balancers()
            albs = []
            for lb in response["LoadBalancers"]:
                lb_data = {
                    "LoadBalancerName": lb["LoadBalancerName"],
                    "LoadBalancerArn": lb["LoadBalancerArn"],
                    "Scheme": lb["Scheme"],
                    "VpcId": lb["VpcId"],
                    "Subnets": lb["AvailabilityZones"],
                    "State": lb["State"]["Code"],
                    "Type": lb["Type"],
                }
                albs.append(lb_data)
            return albs
        except ClientError as e:
            print(f"Error fetching Load Balancers: {e}")
            return []

    def display_resources(self):
        """Fetch and display all resources in a formatted way"""
        print("\n" + "=" * 80)
        print("AWS RESOURCE DISCOVERY")
        print("=" * 80)

        # Fetch VPCs
        print("\n[1] VPCs")
        print("-" * 80)
        vpcs = self.fetch_vpcs()
        for vpc in vpcs:
            name = vpc["Tags"].get("Name", "No Name")
            print(f"  VPC ID: {vpc['VpcId']}")
            print(f"  Name: {name}")
            print(f"  CIDR: {vpc['CidrBlock']}")
            print()

        if not vpcs:
            print("  No VPCs found\n")
            return

        # Let user select a VPC
        selected_vpc = vpcs[0]["VpcId"] if vpcs else None
        if len(vpcs) > 1:
            print(f"Using first VPC: {selected_vpc}\n")

        # Fetch Subnets
        print("[2] SUBNETS")
        print("-" * 80)
        subnets = self.fetch_subnets(vpc_id=selected_vpc)
        for subnet in subnets:
            name = subnet["Tags"].get("Name", "No Name")
            print(f"  Subnet ID: {subnet['SubnetId']}")
            print(f"  Name: {name}")
            print(f"  CIDR: {subnet['CidrBlock']}")
            print(f"  AZ: {subnet['AvailabilityZone']}")
            print()

        # Fetch Security Groups
        print("[3] SECURITY GROUPS")
        print("-" * 80)
        sgs = self.fetch_security_groups(vpc_id=selected_vpc)
        for sg in sgs:
            print(f"  Group ID: {sg['GroupId']}")
            print(f"  Name: {sg['GroupName']}")
            print(f"  Description: {sg['Description']}")
            print()

        # Fetch EC2 Instances
        print("[4] EC2 INSTANCES")
        print("-" * 80)
        instances = self.fetch_ec2_instances()
        for instance in instances:
            name = instance["Tags"].get("Name", "No Name")
            print(f"  Instance ID: {instance['InstanceId']}")
            print(f"  Name: {name}")
            print(f"  Type: {instance['InstanceType']}")
            print(f"  State: {instance['State']}")
            print(f"  VPC: {instance['VpcId']}")
            print()

        # Fetch Load Balancers
        print("[5] EXISTING LOAD BALANCERS (ALBs)")
        print("-" * 80)
        albs = self.fetch_load_balancers()
        if albs:
            for alb in albs:
                print(f"  Name: {alb['LoadBalancerName']}")
                print(f"  ARN: {alb['LoadBalancerArn']}")
                print(f"  Scheme: {alb['Scheme']}")
                print(f"  VPC: {alb['VpcId']}")
                print()
        else:
            print("  No Load Balancers found\n")

        # Export to JSON
        print("\n[6] EXPORTING TO FILE")
        print("-" * 80)
        export_data = {
            "vpcs": vpcs,
            "subnets": subnets,
            "security_groups": sgs,
            "ec2_instances": instances,
            "load_balancers": albs,
        }

        export_file = "aws_resources.json"
        with open(export_file, "w") as f:
            json.dump(export_data, f, indent=2, default=str)

        print(f"✓ Resources exported to: {export_file}")
        print(f"  Use this file to populate project_config.json\n")


if __name__ == "__main__":
    import sys

    region = sys.argv[1] if len(sys.argv) > 1 else "ap-south-1"
    fetcher = AWSResourceFetcher(region=region)
    fetcher.display_resources()
