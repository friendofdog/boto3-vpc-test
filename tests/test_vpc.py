from tests.fixtures.vpc_tests import *

def test_aws_create_vpc(make_ec2_stub, mock_vpc):
    vpc_id = 'vpc-a01106c2'
    cidr_block = '172.16.0.0/16'
    ec2_stub, ec2_obj = make_ec2_stub()
    response = mock_vpc(vpc_id, cidr_block, ec2_stub, ec2_obj)
    assert ec2_obj.vpc['Vpc']['VpcId'] == response['Vpc']['VpcId']

def test_aws_create_internet_gateway(make_ec2_stub, mock_internet_gateway):
    ig_id = 'igw-c0a643a9'
    ec2_stub, ec2_obj = make_ec2_stub()
    response = mock_internet_gateway(ig_id, ec2_stub, ec2_obj)
    assert ec2_obj.ig['InternetGateway']['InternetGatewayId'] == \
        response['InternetGateway']['InternetGatewayId']

def test_aws_create_subnet(make_ec2_stub, mock_vpc, mock_subnet):
    cidr_block = '172.16.1.0/24'
    vpc_id = 'vpc-a01106c2'
    ec2_stub, ec2_obj = make_ec2_stub()
    mock_vpc(vpc_id, cidr_block, ec2_stub, ec2_obj)
    response = mock_subnet(cidr_block, ec2_stub, ec2_obj)
    assert ec2_obj.vpc['Vpc']['VpcId'] == response['Subnet']['VpcId']
