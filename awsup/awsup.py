#!/usr/bin/env python3
from requests import get
import boto3

ip = get('https://api.ipify.org').text

session = boto3.Session(profile_name='uberadminperson') # Specify a profile that has proper permissions to modify security group rules.
ec2 = session.resource('ec2')

security_group = ec2.SecurityGroup('sg-1233235')

for hole in security_group.ip_permissions:
    if (hole["FromPort"] == 22): # I only care about ssh
        for ip_range in hole["IpRanges"]:
            cidr = ip_range['CidrIp']
            security_group.revoke_ingress(
                CidrIp=cidr,
                FromPort=22,
                ToPort=22,
                IpProtocol='tcp')
            print('revoked IP range %s' % (cidr))

security_group.authorize_ingress(
    CidrIp=ip+'/32',
    FromPort=22,
    ToPort=22,
    IpProtocol='tcp'
)
print('authorized IP range %s' % (ip+'/32'))