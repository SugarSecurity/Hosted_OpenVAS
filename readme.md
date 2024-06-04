![Sugar Security Logo](https://assets.sugarsecurity.com/logo.jpg)

An easy way to run [OpenVAS](https://github.com/greenbone/openvas-scanner) inside your AWS account.

A good middle ground between Open Source from Scratch and a Commercial Service

## Minimum Requirements

- [python 3.11+](https://www.python.org/downloads/)

## Recommended Requirements

- [devbox](https://www.jetify.com/devbox/docs/quickstart/)
- [asdf](https://asdf-vm.com/#/core-manage-asdf)
- [poetry](https://python-poetry.org/docs/)
- [awscli](https://aws.amazon.com/cli/)

## Quickstart

- Copy `.env.example` to `.env`
- Fill out `.env` file with your AWS credentials
  - `INSTANCE_TYPE` and `AMI` are optional

```bash
# create virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python -m pip install -r requirements.txt

# create stack if not already created
pulumi preview

# deploy stack
pulumi up

# connect to instance
export SSH_KEY="~/.ssh/id_rsa"
export STACK="<org-name>/<stack-name>"
export IP_ADDR=$(pulumi stack -s "$STACK" output public_ip)
ssh -i "$SSH_KEY" "ec2-user@${IP_ADDR}"

# run openvas

# delete stack
pulumi destroy
```

## Notes

- This is a work in progress, not ready for production
- The _`_main__.py` file uses a simple EC2 User Data Script for setup
- The `__main__.py.wip` file is a work in progress using AWS ECS

## TODO

- Debug user data script
- Use OpenVAS and document
