import boto3

class AwsVpc:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.vpc = ''
        self.ig = ''
        self.sn = ''
        self.sg = ''
        self.rt = ''

    def aws_create_vpc(self, cidr_block):
        vpc = self.ec2_client.create_vpc(
            CidrBlock=cidr_block
        )
        self.vpc = vpc

    def aws_create_internet_gateway(self):
        ig = self.ec2_client.create_internet_gateway()
        self.ig = ig

    def aws_create_subnet(self, vpc_id, cidr_block):
        subnet = self.ec2_client.create_subnet(
            CidrBlock=cidr_block,
            VpcId=vpc_id
        )
        self.sn = subnet

    def aws_create_security_group(self, vpc_id, name, desc):
        security_group = self.ec2_client.create_security_group(
            GroupName=name,
            Description=desc,
            VpcId=vpc_id
        )
        self.sg = security_group

    def aws_create_route_table(self, vpc_id):
        route_table = self.ec2_client.create_route_table(
            VpcId=vpc_id
        )
        self.rt = route_table

    ## assign a name to our VPC
    #def tag_vpc(self):
    #    self.vpc.create_tags(
    #        Tags=[{"Key": "Name", "Value": "my_vpc"}]
    #    )
    #    self.vpc.wait_until_available()

    ## enable public dns hostname so that we can SSH into it later
    #def enable_public_dns(self):
    #    self.ec2_client.modify_vpc_attribute(
    #        VpcId=self.vpc.id,
    #        EnableDnsSupport={'Value': True}
    #    )
    #    self.ec2_client.modify_vpc_attribute(
    #        VpcId=self.vpc.id,
    #        EnableDnsHostnames={'Value': True}
    #    )

    ## attach internet gateway to VPC
    #def attach_internet_gateway(self):
    #    self.vpc.attach_internet_gateway(
    #        InternetGatewayId=self.ig.id
    #    )

    ## create public route on route table
    #def create_public_route_table(self):
    #    self.rt.create_route(
    #        DestinationCidrBlock='0.0.0.0/0',
    #        GatewayId=self.ig.id
    #    )

    ## associate subnet with route table
    #def associate_subnet(self):
    #    self.rt.associate_with_subnet(
    #        SubnetId=self.sn.id
    #    )

    ## allow SSH inbound rule through the VPC on security group
    #def create_ssh_inbound_rule(self):
    #    self.sg.authorize_ingress(
    #        CidrIp='0.0.0.0/0',
    #        IpProtocol='tcp',
    #        FromPort=22,
    #        ToPort=22
    #    )

    ## create SSH key pair and store locally
    #def create_ssh_keys(self):
    #    outfile = open('ec2-keypair.pem', 'w')
    #    key_pair = self.ec2_client.create_key_pair(
    #        KeyName='ec2-keypair'
    #    )
    #    key_pair_out = str(key_pair.key_material)
    #    outfile.write(key_pair_out)

    ## create a linux instance in the subnet
    #def create_linux_instance(self):
    #    self.ec2_client.create_instances(
    #        ImageId='ami-0278fe6949f6b1a06',
    #        InstanceType='t2.micro',
    #        MaxCount=1,
    #        MinCount=1,
    #        NetworkInterfaces=[{
    #            'SubnetId': self.sn.id,
    #            'DeviceIndex': 0,
    #            'AssociatePublicIpAddress': True,
    #            'Groups': [self.sg.group_id]
    #        }],
    #        KeyName='ec2-keypair'
    #    )
