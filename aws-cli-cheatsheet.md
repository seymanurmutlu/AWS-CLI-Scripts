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

**Get EC2 Instances and IP Adresses**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,PublicIpAddress]" --output table
```

**Get Elastic IPs attached to the EC2 instances**
```
aws ec2 describe-addresses --query "Addresses[*].[InstanceId,PublicIp]" --output table
```

**Get Elastic Load Balancers attached to the EC2 instances**
```
aws elb describe-load-balancers --query "LoadBalancerDescriptions[*].[LoadBalancerName,Instances[*].InstanceId]" --output table
```

**Get all EC2s with all private IP addresses**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,PrivateIpAddresses:NetworkInterfaces[*].PrivateIpAddresses[*].PrivateIpAddress}" --output json   
```

**Get all EC2s with all public IP addresses**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,PublicIp:NetworkInterfaces[*].Association.PublicIp}" --output json
```

**Get all EC2s with all ENI IDs**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,NetworkInterfaces:NetworkInterfaces[*].NetworkInterfaceId}" --output json
```

**Get all EC2s with all private ips, public ips, ENI IDs**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,PrivateIpAddresses:NetworkInterfaces[*].PrivateIpAddresses[*].PrivateIpAddress,PublicIps:NetworkInterfaces[*].Association.PublicIp,NetworkInterfaceIds:NetworkInterfaces[*].NetworkInterfaceId}" --output json
```

**Get all EC2s with all ENI Details**
```
aws ec2 describe-instances --query "Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,NetworkInterfaces:NetworkInterfaces}" --output json > ec2_instances_with_enis.json
```

**Get all Elastic IPs with attached instances and Elastic IP Names**
```
aws ec2 describe-addresses --query "Addresses[*].{InstanceId:InstanceId,Name:Tags[?Key=='Name']|[0].Value,ElasticIp:PublicIp}" --output json
```

**Get all Classic Load Balancer with attached ip**
```
aws elb describe-load-balancers --query "LoadBalancerDescriptions[*].{LoadBalancerName:LoadBalancerName,Instances:Instances[*].InstanceId}" --output json > classic_load_balancers.json
```

**Get all Application and Network Load Balancer with attached instances**
```
aws elbv2 describe-load-balancers --query "LoadBalancers[*].{LoadBalancerName:LoadBalancerName,LoadBalancerArn:LoadBalancerArn}" --output json
```
