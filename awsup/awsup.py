#!/usr/bin/env python3
import argparse
import os
import logging
from getip import getip
import boto3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

argparser = argparse.ArgumentParser(description='Update AWS EC2 to allow your current IP through the security groups.',
                                    epilog='The paramters --profile and --security-group can be set with environment variables AWS_PROFILE and AWS_SECURITY_GROUP, respecctively')
argparser.add_argument('-p', '--profile', help='aws profile name from ~/.aws/credentials.', default=os.environ.get('AWS_PROFILE'))
argparser.add_argument('-s', '--security-group', help='aws ec2 security group ID to run against.', default=os.environ.get('AWS_SECURITY_GROUP'))
args = argparser.parse_args()

logging.debug('profile: %s' % (args.profile))
logging.debug('security_group: %s' % (args.security_group))

if (args.profile is None) or (args.security_group is None):
    exit(argparser.print_help())

ip = getip()
logging.debug('Your current IP address is: %s' % (ip))

session = boto3.Session(profile_name=args.profile)
ec2 = session.resource('ec2')

security_group = ec2.SecurityGroup(args.security_group)

for hole in security_group.ip_permissions:
    if (hole['FromPort'] == 22): # We only care about ssh on port 22.
        for ip_range in hole['IpRanges']:
            cidr = ip_range['CidrIp']
            security_group.revoke_ingress(
                CidrIp=cidr,
                FromPort=22,
                ToPort=22,
                IpProtocol='tcp')
            logging.info('revoked IP range %s' % (cidr))

security_group.authorize_ingress(
    CidrIp=ip+'/32',
    FromPort=22,
    ToPort=22,
    IpProtocol='tcp'
)
logging.info('authorized IP range %s' % (ip+'/32'))