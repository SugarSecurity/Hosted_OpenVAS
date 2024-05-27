![Sugar Security Logo](https://assets.sugarsecurity.com/logo.jpg)

An easy way to run [OpenVAS](https://github.com/greenbone/openvas-scanner) inside your AWS account.

A good middle ground between Open Source from Scratch and a Commercial Service

## how-to

1. `pip install pulumi`
2. `pulumi up`

## notes

- This is a work in progress, not ready for production
- The __main__.py file uses a simple EC2 User Data Script for setup
- The __main__.py.wip file is a work in progress using AWS ECS