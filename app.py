import vpc

if __name__ == "__main__":
    aws_vpc = vpc.AwsVpc()
    aws_vpc.tag_vpc()
    aws_vpc.enable_public_dns()
    aws_vpc.attach_internet_gateway()
    aws_vpc.create_public_route_table()
    aws_vpc.associate_subnet()
    aws_vpc.create_ssh_inbound_rule()
    aws_vpc.create_ssh_keys()
    aws_vpc.create_linux_instance()
