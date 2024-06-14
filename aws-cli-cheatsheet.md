# AWS CLI Cheatsheet

**Get all the security groups with IDs**
```
aws ec2 describe-security-groups --query 'SecurityGroups[*].GroupId' --output text
```
**Get all the security groups with ID and Names**
```
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId, GroupName]' --output json
```
**Get all the prefix list with ID and Names**
```
aws ec2 describe-managed-prefix-lists --query 'PrefixLists[*].[PrefixListId, PrefixListName]' --output json
```

**Get all the attached instances as list to given Security Group ID**
```
aws ec2 describe-instances --filters Name=instance.group-id,Values=<SECURITY GROUP ID> --query "Reservations[*].Instances[*].{InstanceID:InstanceId,InstanceType:InstanceType,State:State.Name,Name:Tags[?Key=='Name']|[0].Value}" --output table
```

**Get security group rule id details**
```
aws ec2 describe-security-group-rules --security-group-rule-ids <SECURITY GROUP RULE ID>  --output json 
```