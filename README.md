AWS VPC Management Tool
=======================

This tool allows the provisioning and management of VPCs and related resources
and services on AWS. It uses the official Python SDK, Boto3.

Testing is greatly emphasised, as without it real (billable) resources would be
created every time the script runs. Botocore is therefore used to ensure that
the applications runs without touching the live API.

By using this tool outside of tests, the following resources might be created:

- VPCs
- internet gateways
- subnets
- security groups
- route tables

Usage
-----

### Testing

Running the `Test` Bash script will activate the virtual environment and run
all tests using PyTest.

### Live

Running `app.py` will run all methods associated with creating a VPC and create
live resources.

Requirements
------------

- Python3
- Bash (for testing and development)
- Local AWS credentials

For instructions on how to set up AWS credentials, see following article:

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

Credits
-------

This project is based on the below tutorial:

https://blog.ipswitch.com/how-to-create-and-configure-an-aws-vpc-with-python

Script to set up virtual environment and testing:

https://github.com/0cjs/sedoc/blob/master/lang/python/runtime/activate
