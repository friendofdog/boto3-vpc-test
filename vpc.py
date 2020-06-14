import boto3

class AwsVpc:
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.vpc = ''
        self.internetgateway = ''
        self.subnet = ''
        self.securitygroup = ''
        self.routetable = ''

    def aws_create_vpc(self, ip='172.10.0.0/16'):
        vpc = self.ec2.create_vpc(
            CidrBlock=ip
        )
        self.vpc = vpc

    def aws_create_internet_gateway(self):
        internetgateway = self.ec2.create_internet_gateway()
        self.internetgateway = internetgateway

    def aws_create_subnet(self):
        self.subnet = self.ec2.create_subnet(
            CidrBlock='172.16.1.0/24',
            VpcId=self.vpc.id
        )

    def aws_create_security_group(self):
        self.securitygroup = self.ec2.create_security_group(
            GroupName='SSH-ONLY',
            Description='only allow SSH traffic',
            VpcId=self.vpc.id
        )

    def aws_create_route_table(self):
        self.routetable = self.vpc.create_route_table()

    # assign a name to our VPC
    def tag_vpc(self):
        self.vpc.create_tags(
            Tags=[{"Key": "Name", "Value": "my_vpc"}]
        )
        self.vpc.wait_until_available()

    # enable public dns hostname so that we can SSH into it later
    def enable_public_dns(self):
        self.ec2_client.modify_vpc_attribute(
            VpcId=self.vpc.id,
            EnableDnsSupport={'Value': True}
        )
        self.ec2_client.modify_vpc_attribute(
            VpcId=self.vpc.id,
            EnableDnsHostnames={'Value': True}
        )

    # attach internet gateway to VPC
    def attach_internet_gateway(self):
        self.vpc.attach_internet_gateway(
            InternetGatewayId=self.internetgateway.id
        )

    # create public route on route table
    def create_public_route_table(self):
        self.routetable.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=self.internetgateway.id
        )

    # associate subnet with route table
    def associate_subnet(self):
        self.routetable.associate_with_subnet(
            SubnetId=self.subnet.id
        )

    # allow SSH inbound rule through the VPC on security group
    def create_ssh_inbound_rule(self):
        self.securitygroup.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22
        )

    # create SSH key pair and store locally
    def create_ssh_keys(self):
        outfile = open('ec2-keypair.pem', 'w')
        key_pair = self.ec2.create_key_pair(
            KeyName='ec2-keypair'
        )
        key_pair_out = str(key_pair.key_material)
        outfile.write(key_pair_out)

    # create a linux instance in the subnet
    def create_linux_instance(self):
        self.ec2.create_instances(
            ImageId='ami-0278fe6949f6b1a06',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            NetworkInterfaces=[{
                'SubnetId': self.subnet.id,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [self.securitygroup.group_id]
            }],
            KeyName='ec2-keypair'
        )
