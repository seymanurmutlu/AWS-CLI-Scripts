# Gets Security Groups with GroupId,GroupName,Description,Attached Instance ID,Attached Instance IP,Attached Instance Name,Direction,IpProtocol,FromPort,ToPort,CidrIp and saves to a JSON file.
import json
import subprocess
import csv

def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_json_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def get_attached_instances(security_group_id):
    # List all instances
    result = subprocess.run(['aws', 'ec2', 'describe-instances'], stdout=subprocess.PIPE)
    instances = json.loads(result.stdout)

    # Save the instances data to a file
    json_filename = 'instances.json'
    save_json_to_file(instances, json_filename)

    # Load the instances data from the file
    instances = load_json_from_file(json_filename)

    # Find instances that are attached to the specified security group
    attached_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance.get('SecurityGroups', []):
                if sg['GroupId'] == security_group_id:
                        instance_id = instance['InstanceId']
                        private_ip_address = instance['PrivateIpAddress']
                        instance_name = ''
                        for tag in instance.get('Tags', []):
                            if tag['Key'] == 'Name':
                                instance_name = tag['Value']
                                break
                        attached_instances.append(f"{instance_id}@{private_ip_address}@{instance_name}")
    
    return attached_instances

def process_permission(permission, direction):
    ip_protocol = permission['IpProtocol']
    from_port = permission.get('FromPort', '')
    to_port = permission.get('ToPort', '')

    # Handle multiple IP ranges
    ranges = permission.get('IpRanges', [])
    if not ranges:
        return [[direction, ip_protocol, from_port, to_port, '']]

    return [[direction, ip_protocol, from_port, to_port, ip_range.get('CidrIp', '')] for ip_range in ranges]


# Execute the AWS CLI command for security groups
sg_result = subprocess.run(['aws', 'ec2', 'describe-security-groups'], stdout=subprocess.PIPE)
security_groups = json.loads(sg_result.stdout)

# Define the CSV file name
csv_file = "security_groups.csv"

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['GroupId', 'GroupName', 'Description', 'Direction', 'IpProtocol', 'FromPort', 'ToPort', 'CidrIp', 'AttachedInstance'])

    # Process each security group
    for group in security_groups['SecurityGroups']:
        group_id = group['GroupId']
        attached_instances = get_attached_instances(group_id)
        common_data = [group.get('GroupName', ''), group.get('Description', '')]

        # Process egress permissions (outbound)
        for permission in group['IpPermissionsEgress']:
            for row_data in process_permission(permission, 'Outbound'):
                for instance in attached_instances:
                    writer.writerow([group_id] + common_data + [instance] + row_data)

        # Process ingress permissions (inbound)
        for permission in group['IpPermissions']:
            for row_data in process_permission(permission, 'Inbound'):
                for instance in attached_instances:
                    writer.writerow([group_id] + common_data + [instance] + row_data)



print(f"CSV file '{csv_file}' has been created.")


