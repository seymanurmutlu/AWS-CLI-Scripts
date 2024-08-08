import boto3
import pandas as pd

# Use this code is you are login aws cli with "aws sso login"
# AWS profiles, should be edited due to profile names in local device 
profiles = [
    "profile1", "profile2", "profile3", "profile4", "profile5",
    "profile6", "profile7", "profile8", "profile9", "profile10",
    "profile11", "profile12"
]

def get_session(profile_name):
    return boto3.Session(profile_name=profile_name)

def get_ec2_instances(session):
    ec2_client = session.client('ec2')
    paginator = ec2_client.get_paginator('describe_instances')
    response_iterator = paginator.paginate()
    
    instances = []
    for response in response_iterator:
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)
    
    return instances

def get_elastic_ips(session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_addresses()
    return response['Addresses']

def get_classic_load_balancers(session):
    elb_client = session.client('elb')
    response = elb_client.describe_load_balancers()
    return response['LoadBalancerDescriptions']

def get_application_load_balancers(session):
    elbv2_client = session.client('elbv2')
    response = elbv2_client.describe_load_balancers()
    return response['LoadBalancers']

data = []

for profile in profiles:
    print(f"Fetching data for profile: {profile}")
    session = get_session(profile)
    
    # Get EC2 instances
    instances = get_ec2_instances(session)
    
    # Get Elastic IPs
    elastic_ips = get_elastic_ips(session)
    elastic_ip_dict = {}
    for eip in elastic_ips:
        instance_id = eip.get('InstanceId')
        if instance_id:
            if instance_id in elastic_ip_dict:
                elastic_ip_dict[instance_id].append(eip['PublicIp'])
            else:
                elastic_ip_dict[instance_id] = [eip['PublicIp']]
    
    # Get Classic Load Balancers
    classic_lbs = get_classic_load_balancers(session)
    classic_lb_dict = {}
    for lb in classic_lbs:
        lb_name = lb['LoadBalancerName']
        for instance in lb['Instances']:
            instance_id = instance['InstanceId']
            if instance_id in classic_lb_dict:
                classic_lb_dict[instance_id].append(lb_name)
            else:
                classic_lb_dict[instance_id] = [lb_name]

    # Get Application Load Balancers
    app_net_lbs = get_application_load_balancers(session)
    app_net_lb_dict = {}
    lb_arn_to_name = {lb['LoadBalancerArn']: lb['LoadBalancerName'] for lb in app_net_lbs}
    for lb in app_net_lbs:
        lb_arn = lb['LoadBalancerArn']
        lb_name = lb_arn_to_name[lb_arn]
        app_net_lb_dict[lb_arn] = lb_name

    for instance in instances:
        instance_id = instance.get('InstanceId', 'N/A')
        name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
        private_ips = [ip['PrivateIpAddress'] for eni in instance.get('NetworkInterfaces', []) for ip in eni.get('PrivateIpAddresses', [])]
        public_ips = [eni.get('Association', {}).get('PublicIp', 'N/A') for eni in instance.get('NetworkInterfaces', []) if 'Association' in eni]
        enis = [eni['NetworkInterfaceId'] for eni in instance.get('NetworkInterfaces', [])]
        elastic_ips = elastic_ip_dict.get(instance_id, [])
        classic_lbs = classic_lb_dict.get(instance_id, [])
        app_net_lbs = [app_net_lb_dict.get(eni, 'N/A') for eni in enis]

        data.append({
            'Instance ID': instance_id,
            'Name': name,
            'Private IPs': ', '.join(private_ips),
            'Public IPs': ', '.join(public_ips),
            'Elastic IPs': ', '.join(elastic_ips),
            'ENIs': ', '.join(enis),
            'Classic Load Balancers': ', '.join(classic_lbs),
            'App/Net Load Balancers': ', '.join(app_net_lbs)
        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('ec2_complete_details.csv', index=False)

# Print the DataFrame
print(df)
