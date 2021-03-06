#!/usr/bin/env python3
import argparse
import boto3
import logging
import os
from requests import get

def get_args():
    argparser = argparse.ArgumentParser(description='Update AWS EC2 to allow your current IP through the security groups.',
                                        epilog='The paramters --profile and --security-group can be set with environment variables AWS_PROFILE and AWS_SECURITY_GROUP, respecctively')
    argparser.add_argument('-p', '--profile', help='aws profile name from ~/.aws/credentials.', default=os.environ.get('AWS_PROFILE'))
    argparser.add_argument('-o', '--port', dest='port_number', help='Port number to modify. Defaults to 22', default=22)
    argparser.add_argument('-i', '--ip', dest='ip_address', help='Current IP address or address to allow', default=get_my_ip())
    argparser.add_argument('-s', '--security-group', dest='security_group_id', help='AWS EC2 security group ID to run against.', default=os.environ.get('AWS_SECURITY_GROUP_ID'))
    argparser.add_argument('-v', '--verbose', action='store_true', help='Show full debug output.')
    args = argparser.parse_args()
    if (args.profile is None) or (args.security_group_id is None):
        exit(argparser.print_help())
    
    if args.verbose:
        logging_level=logging.DEBUG
    else:
        logging_level=logging.INFO

    logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('profile: %s' % (args.profile))
    logging.debug('security_group_id: %s' % (args.security_group_id))

    return args

def get_ec2_session(profile):
    session = boto3.Session(profile_name=profile)
    return session.resource('ec2')

def revoke_priors(security_group, port):
    for hole in security_group.ip_permissions:
        if (hole['FromPort'] == port):
            for ip_range in hole['IpRanges']:
                cidr = ip_range['CidrIp']
                security_group.revoke_ingress(
                    CidrIp=cidr,
                    FromPort=port,
                    ToPort=port,
                    IpProtocol='tcp')
                logging.info('revoked IP range %s' % (cidr))

def allow_current(ip, security_group, port):
    security_group.authorize_ingress(
        CidrIp=ip+'/32',
        FromPort=port,
        ToPort=port,
        IpProtocol='tcp'
    )
    logging.info('authorized IP range %s on port %s.' % (ip+'/32', port))

def get_my_ip():
    return get('https://api.ipify.org').text

def main():
    args = get_args()
    logging.info('Your current IP address is: %s' % (args.ip_address))
    ec2 = get_ec2_session(args.profile)
    security_group = ec2.SecurityGroup(args.security_group_id)
    revoke_priors(security_group, args.port_number)
    allow_current(args.ip_address, security_group, args.port_number)


if __name__ == "__main__":
    main()
