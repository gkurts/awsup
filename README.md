# awsup
AWS EC2 security group updater thingy

usage: awsup.py [-h] [-p PROFILE] [-s SECURITY_GROUP_ID] [-v]

Update AWS EC2 to allow your current IP through the security groups.

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        aws profile name from ~/.aws/credentials.
  -s SECURITY_GROUP_ID, --security-group SECURITY_GROUP_ID
                        AWS EC2 security group ID to run against.
  -v, --verbose         Show full debug output.

The paramters --profile and --security-group can be set with environment
variables AWS_PROFILE and AWS_SECURITY_GROUP, respecctively
