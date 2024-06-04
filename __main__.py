#!/usr/bin/env python

import boto3
import pulumi_aws as aws
from pulumi import export
from decouple import config
# from pathlib import Path

# Define EC2 instance details
# cf. https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#AMICatalog:
instance_type = config("INSTANCE_TYPE", default="t2.micro")
ami = config("AMI", default="ami-00beae93a2d981137")

# TODO: debug the user_data script
# Define the User Data script
# user_data = Path("user_data.sh").read_text()
user_data = """#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo yum install -y ca-certificates curl gnupg
curl -f -O https://greenbone.github.io/docs/latest/_static/setup-and-start-greenbone-community-edition.sh
chmod u+x setup-and-start-greenbone-community-edition.sh
./setup-and-start-greenbone-community-edition.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
export DOWNLOAD_DIR=$HOME/greenbone-community-container
mkdir -p $DOWNLOAD_DIR
cd $DOWNLOAD_DIR
curl -f -L https://greenbone.github.io/docs/latest/_static/docker-compose-22.4.yml -o docker-compose.yml
sudo docker-compose -f docker-compose.yml -p greenbone-community-edition pull
sudo docker-compose -f docker-compose.yml -p greenbone-community-edition up -d
"""

# Create a boto3 session
session = boto3.Session(
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_REGION", default="us-east-1"),
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
