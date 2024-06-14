## Gets prefixlists id and name as json format and converts it to a csv file 
import subprocess
import json
import csv

# Run AWS CLI command to describe prefix lists and get JSON output
aws_cli_command = "aws ec2 describe-managed-prefix-lists --query 'PrefixLists[*].[PrefixListId, PrefixListName]'  --profile AWS_ReadOnly-853713009882 --output json"
aws_cli_process = subprocess.Popen(aws_cli_command, shell=True, stdout=subprocess.PIPE)
aws_cli_output, _ = aws_cli_process.communicate()
aws_cli_output = aws_cli_output.decode("utf-8")

# Load JSON data
data = json.loads(aws_cli_output)

# Specify the output CSV file for prefix lists
csv_file = 'prefix_lists_ids_and_names_output.csv'

# Write CSV header
csv_header = ["PrefixListId", "PrefixListName"]
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Write each row to the CSV file
    for row in data:
        writer.writerow(row)

print(f"CSV file '{csv_file}' has been created.")
