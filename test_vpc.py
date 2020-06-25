import pytest
from botocore.stub import Stubber
from vpc import AwsVpc


@pytest.fixture
def make_ec2_stub():
    def _make_ec2_stub(interface):
        ec2_obj = AwsVpc()
        service = {
            'resource': ec2_obj.ec2.meta.client,
            'client': ec2_obj.ec2_client
        }
        ec2_stub = Stubber(service[interface])
        return ec2_stub, ec2_obj

    yield _make_ec2_stub


@pytest.fixture
def mock_vpc():
    def _mock_vpc(vpc_id, cidr_block, ec2_stub, ec2_obj):
        response = {
            'Vpc': {
                'CidrBlock': cidr_block,
                'VpcId': vpc_id,
            }
        }

        expected_params = {
            'CidrBlock': cidr_block
        }

        ec2_stub.add_response(
            'create_vpc',
            response,
            expected_params
        )

        ec2_stub.activate()
        ec2_obj.aws_create_vpc(cidr_block)
        return response

    return _mock_vpc


@pytest.fixture
def mock_internet_gateway():
    def _mock_internet_gateway(ig_id, ec2_stub, ec2_obj):
        response = {
            'InternetGateway': {
                'InternetGatewayId': ig_id
            }
        }

        ec2_stub.add_response(
            'create_internet_gateway',
            response,
            {}
        )

        ec2_stub.activate()
        ec2_obj.aws_create_internet_gateway()
        return response

    return _mock_internet_gateway


@pytest.fixture
def mock_subnet():
    def _mock_subnet(cidr_block, ec2_stub, ec2_obj):
        vpc_id = ec2_obj.vpc['Vpc']['VpcId']

        response = {
            'Subnet': {
                'CidrBlock': cidr_block,
                'VpcId': vpc_id,
            }
        }
        expected_params = {
            'CidrBlock': cidr_block,
            'VpcId': vpc_id
        }

        ec2_stub.add_response(
            'create_subnet',
            response,
            expected_params
        )

        ec2_stub.activate()
        ec2_obj.aws_create_subnet(vpc_id, cidr_block)
        return response

    return _mock_subnet


def test_aws_create_vpc(make_ec2_stub, mock_vpc):
    vpc_id = 'vpc-a01106c2'
    cidr_block = '172.16.0.0/16'
    ec2_stub, ec2_obj = make_ec2_stub('resource')
    response = mock_vpc(vpc_id, cidr_block, ec2_stub, ec2_obj)
    assert ec2_obj.vpc.id == response['Vpc']['VpcId']

def test_aws_create_internet_gateway(make_ec2_stub, mock_internet_gateway):
    ig_id = 'igw-c0a643a9'
    ec2_stub, ec2_obj = make_ec2_stub('resource')
    response = mock_internet_gateway(ig_id, ec2_stub, ec2_obj)
    assert ec2_obj.internetgateway.id == \
        response['InternetGateway']['InternetGatewayId']

def test_aws_create_subnet(make_ec2_stub, mock_vpc, mock_subnet):
    cidr_block = '172.16.1.0/24'
    vpc_id = 'vpc-a01106c2'
    ec2_stub, ec2_obj = make_ec2_stub('client')
    mock_vpc(vpc_id, cidr_block, ec2_stub, ec2_obj)
    response = mock_subnet(cidr_block, ec2_stub, ec2_obj)
    assert ec2_obj.vpc['Vpc']['VpcId'] == response['Subnet']['VpcId']
