# Gets all security group ids and names and saves to csv.
import subprocess
import json
import csv

# Run AWS CLI command to describe security groups and get JSON output
aws_cli_command = "aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId, GroupName]' --output json"
aws_cli_process = subprocess.Popen(aws_cli_command, shell=True, stdout=subprocess.PIPE)
aws_cli_output, _ = aws_cli_process.communicate()
aws_cli_output = aws_cli_output.decode("utf-8")

# Load JSON data
data = json.loads(aws_cli_output)

# Specify the output CSV file
csv_file = 'sg-id-and-name.csv'

# Write CSV header
csv_header = ["GroupId", "GroupName"]
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Write each row to the CSV file
    for row in data:
        writer.writerow(row)

print(f"CSV file '{csv_file}' has been created.")
