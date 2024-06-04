#!/usr/bin/env python

import boto3
import pulumi_aws as aws
from pulumi import export
from decouple import config
from pathlib import Path

# Define EC2 instance details
# cf. https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#AMICatalog:
instance_type = config("INSTANCE_TYPE", default="t2.micro")
ami = config("AMI", default="ami-00beae93a2d981137")

# Define the User Data script
user_data = Path("user_data.sh").read_text()

# Create a boto3 session
session = boto3.Session(
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_REGION"),
)

# Create a boto3 client
ec2 = session.client('ec2')

# Get the security group ID
security_groups = ec2.describe_security_groups()
security_group_id = security_groups['SecurityGroups'][0]['GroupId']  # First security group

# Get the key pair name
key_pairs = ec2.describe_key_pairs()
key_name = key_pairs['KeyPairs'][0]['KeyName']      # First key pair

# Create an EC2 instance
ec2_instance = aws.ec2.Instance(
    "greenbone-instance",
    instance_type=instance_type,
    ami=ami,
    user_data=user_data,
    tags={
        "Name": "GreenboneCommunityEdition",
    },
    vpc_security_group_ids=[security_group_id],     # Use the security group ID
    key_name=key_name,                              # Use the key pair name
)

# Export the instance's public IP
export("public_ip", ec2_instance.public_ip)
export("public_dns", ec2_instance.public_dns)
