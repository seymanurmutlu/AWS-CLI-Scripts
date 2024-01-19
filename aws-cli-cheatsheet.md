**Get all the security groups with IDs**

aws ec2 describe-security-groups --query 'SecurityGroups[*].GroupId' --output text

