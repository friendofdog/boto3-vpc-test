import pytest
from botocore.stub import Stubber
from vpc import AwsVpc


@pytest.fixture
def make_ec2_stub():
    def _make_ec2_stub(key):
        vpc_obj = AwsVpc()
        service = {
            'resource': vpc_obj.ec2.meta.client,
            'client': vpc_obj.ec2_client
        }
        ec2_stub = Stubber(service[key])
        return ec2_stub, vpc_obj

    yield _make_ec2_stub


def test_aws_create_vpc(make_ec2_stub):
    ec2_stub, vpc_obj = make_ec2_stub('resource')

    cidr_block = '172.16.0.0/16'

    response = {
        'Vpc': {
            'CidrBlock': cidr_block,
            'VpcId': 'vpc-a01106c2',
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

    vpc_obj.aws_create_vpc(cidr_block)

    assert vpc_obj.vpc.id == response['Vpc']['VpcId']

def test_aws_create_internet_gateway(make_ec2_stub):
    ec2_stub, vpc_obj = make_ec2_stub('resource')

    response = {
        'InternetGateway': {
            'InternetGatewayId': 'igw-c0a643a9'
        }
    }

    ec2_stub.add_response(
        'create_internet_gateway',
        response,
        {}
    )

    ec2_stub.activate()

    vpc_obj.aws_create_internet_gateway()

    assert vpc_obj.internetgateway.id == \
        response['InternetGateway']['InternetGatewayId']
