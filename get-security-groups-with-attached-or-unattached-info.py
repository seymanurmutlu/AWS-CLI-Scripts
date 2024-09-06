import boto3
import csv

def get_security_groups():
    # Boto3 EC2 client oluşturma
    ec2 = boto3.client('ec2')

    # Tüm güvenlik gruplarını alma
    all_security_groups = ec2.describe_security_groups()['SecurityGroups']
    
    # Tüm network arayüzlerini (network interfaces) alma
    network_interfaces = ec2.describe_network_interfaces()['NetworkInterfaces']
    
    # Network arayüzlerine bağlı güvenlik gruplarını çıkarma
    attached_security_groups = set()
    for interface in network_interfaces:
        for sg in interface['Groups']:
            attached_security_groups.add(sg['GroupId'])
    
    # Bağlı ve bağlı olmayan güvenlik gruplarını saklamak için listeler
    security_groups_list = []

    # Güvenlik gruplarını kategorize etme ve CSV için hazırlama
    for sg in all_security_groups:
        sg_info = {
            'GroupId': sg['GroupId'],
            'GroupName': sg.get('GroupName', 'N/A'),
            'Description': sg.get('Description', 'N/A'),
            'Attached': 'Yes' if sg['GroupId'] in attached_security_groups else 'No'
        }
        security_groups_list.append(sg_info)

    return security_groups_list

def write_to_csv(security_groups, filename='security_groups.csv'):
    # CSV dosyasına yazma
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['GroupId', 'GroupName', 'Description', 'Attached'])
        writer.writeheader()
        writer.writerows(security_groups)
    print(f"Security groups have been written to {filename}")

def main():
    # Güvenlik gruplarını alma
    security_groups = get_security_groups()
    
    # CSV'ye yazma
    write_to_csv(security_groups)

if __name__ == "__main__":
    main()
