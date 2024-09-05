import json
import subprocess
import csv

def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_json_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_attached_instances(security_group_id, instances):
    attached_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance.get('SecurityGroups', []):
                if sg['GroupId'] == security_group_id:
                    instance_id = instance['InstanceId']
                    private_ip_address = instance.get('PrivateIpAddress', 'N/A')
                    instance_name = ''
                    for tag in instance.get('Tags', []):
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break
                    attached_instances.append(f"{instance_id}@{private_ip_address}@{instance_name}")
    return attached_instances

def write_to_csv(file, data):
    with open(file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def process_security_group_rule(rule, group_id, instances, csv_file):
    attached_instances = get_attached_instances(group_id, instances)
    direction = 'Inbound' if rule['IsEgress'] == False else 'Outbound'
    
    row_data = [
        rule.get('SecurityGroupRuleId'), group_id, direction, rule['IpProtocol'],
        rule.get('FromPort', ''), rule.get('ToPort', ''),
        rule.get('CidrIpv4', ''), rule.get('Description', ''),
        rule.get('PrefixListId', ''), 
        '|'.join([tag['Value'] for tag in rule.get('Tags', [])])
    ]

    for instance in attached_instances:
        data = row_data + [instance]
        print(data)
        write_to_csv(csv_file, data)

def get_security_group_data(profile, csv_file):
    print(f"Fetching data for profile: {profile}")
    
    # Execute the AWS CLI command for security group rules
    sg_result = subprocess.run(['aws', 'ec2', 'describe-security-group-rules', '--profile', profile], stdout=subprocess.PIPE)
    security_group_rules = json.loads(sg_result.stdout)

    # List all instances
    instances_result = subprocess.run(['aws', 'ec2', 'describe-instances', '--profile', profile], stdout=subprocess.PIPE)
    instances = json.loads(instances_result.stdout)

    # Process each security group rule
    for rule in security_group_rules['SecurityGroupRules']:
        group_id = rule['GroupId']
        process_security_group_rule(rule, group_id, instances, csv_file)

# List of AWS profiles to iterate over
aws_profiles = ['profile1', 'profile2', 'profile3']  # Add your AWS profiles here

# Define the CSV file name
csv_file = "security_group_rules.csv"

# Write the header to the CSV file
write_to_csv(csv_file, ['SecurityGroupId', 'GroupId', 'Direction', 'IpProtocol', 'FromPort', 'ToPort', 'CidrIp', 'Description', 'PrefixListId', 'Tags', 'AttachedInstance'])

# Iterate over each AWS profile and fetch the security group data
for profile in aws_profiles:
    get_security_group_data(profile, csv_file)

print(f"CSV file '{csv_file}' has been created.")
