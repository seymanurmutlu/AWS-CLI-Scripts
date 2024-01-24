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
