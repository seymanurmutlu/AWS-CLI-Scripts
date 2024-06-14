import subprocess
import json
import csv

def get_security_group_rules():
    # Run the AWS CLI command to describe security group rules and get the output as JSON
    result = subprocess.run(
        ['aws', 'ec2', 'describe-security-group-rules', '--query', 'SecurityGroupRules[*].{RuleID:SecurityGroupRuleId,Protocol:IpProtocol}', '--output', 'json'],
        capture_output=True,
        text=True
    )

    # Load the JSON output
    data = json.loads(result.stdout)

    return data

def save_to_csv(rules, file_path):
    # Define the CSV file header
    header = ['RuleID', 'Protocol']

    # Write to the CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(rules)

if __name__ == '__main__':
    rules = get_security_group_rules()
    save_to_csv(rules, 'security_group_rules.csv')
    print("Data has been saved to security_group_rules.csv")
