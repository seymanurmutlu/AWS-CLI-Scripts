#get-instance-id-and-name-to-csv.py
import subprocess
import json
import csv

def get_instance_names_and_ids():
    # Run the AWS CLI command to describe instances and get the output as JSON
    result = subprocess.run(
        ['aws', 'ec2', 'describe-instances', '--query', 'Reservations[*].Instances[*].{InstanceId:InstanceId, Tags:Tags}', '--output', 'json'],
        capture_output=True,
        text=True
    )

    # Load the JSON output
    data = json.loads(result.stdout)

    instances = []

    # Process each reservation and instance
    for reservation in data:
        for instance in reservation:
            instance_id = instance['InstanceId']
            instance_name = None
            
            # Check for tags and get the 'Name' tag if it exists
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break
            
            instances.append({'InstanceId': instance_id, 'Name': instance_name})

    return instances

def save_to_csv(instances, file_path):
    # Define the CSV file header
    header = ['InstanceId', 'Name']

    # Write to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(instances)

if __name__ == '__main__':
    instances = get_instance_names_and_ids()
    save_to_csv(instances, 'ec2_instances.csv')
    print("Data has been saved to ec2_instances.csv")