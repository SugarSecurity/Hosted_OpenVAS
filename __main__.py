import pulumi
import pulumi_aws as aws

# Define EC2 instance details
instance_type = "t2.medium"
ami = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (for example, update to latest if needed)

# Define the User Data script
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

# Create an EC2 instance
ec2_instance = aws.ec2.Instance("greenbone-instance",
    instance_type=instance_type,
    ami=ami,
    user_data=user_data,
    tags={
        "Name": "GreenboneCommunityEdition",
    },
    vpc_security_group_ids=[security_group.id],  # Add your security group ID here
    key_name="your-key-pair-name",  # Replace with your key pair name
)

# Export the instance's public IP
pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("public_dns", ec2_instance.public_dns)