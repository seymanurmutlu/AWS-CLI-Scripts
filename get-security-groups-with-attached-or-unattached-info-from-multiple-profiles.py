import boto3
import csv
import os

# AWS profillerini burada tanımla
aws_profiles = [
    "profile-1", "profile-2",
    "profile-3", "profile-4",
]

def get_security_groups(profile_name):
    # Boto3 session oluşturma ve client başlatma
    session = boto3.Session(profile_name=profile_name)
    ec2 = session.client('ec2')

    # Tüm güvenlik gruplarını alma
    all_security_groups = ec2.describe_security_groups()['SecurityGroups']
    
    # Tüm network arayüzlerini (network interfaces) alma
    network_interfaces = ec2.describe_network_interfaces()['NetworkInterfaces']
    
    # Network arayüzlerine bağlı güvenlik gruplarını çıkarma
    attached_security_groups = set()
    for interface in network_interfaces:
        for sg in interface['Groups']:
            attached_security_groups.add(sg['GroupId'])
    
    # Güvenlik gruplarını kategorize etme ve listeye ekleme
    security_groups_list = []
    for sg in all_security_groups:
        sg_info = {
            'GroupId': sg['GroupId'],
            'GroupName': sg.get('GroupName', 'N/A'),
            'Description': sg.get('Description', 'N/A'),
            'Attached': 'Yes' if sg['GroupId'] in attached_security_groups else 'No',
            'Profile': profile_name
        }
        security_groups_list.append(sg_info)

    return security_groups_list

# path ismini directory_path'e gir
def write_to_csv(security_groups, profile_name, directory_path='/path'):
    # Klasörün var olup olmadığını kontrol et ve yoksa oluştur
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    # Her profil için ayrı bir CSV dosyası oluştur
    filename = os.path.join(directory_path, f'security_groups_{profile_name}.csv')

    # CSV dosyasına yazma
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['GroupId', 'GroupName', 'Description', 'Attached', 'Profile'])
        writer.writeheader()
        writer.writerows(security_groups)
    print(f"Security groups for profile {profile_name} have been written to {filename}")

#path ismini directory_path'e gir
def merge_csv_files(directory_path='/path', output_filename='merged_security_groups.csv'):
    merged_data = []
    # Klasördeki tüm CSV dosyalarını oku ve birleştir
    for profile_name in aws_profiles:
        input_filename = os.path.join(directory_path, f'security_groups_{profile_name}.csv')
        if os.path.exists(input_filename):
            with open(input_filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    merged_data.append(row)

    # Birleştirilmiş verileri tek bir CSV dosyasına yaz
    output_file_path = os.path.join(directory_path, output_filename)
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['GroupId', 'GroupName', 'Description', 'Attached', 'Profile'])
        writer.writeheader()
        writer.writerows(merged_data)
    print(f"Merged CSV has been written to {output_file_path}")

def main():
    # Her profil için güvenlik gruplarını al ve CSV'ye yaz
    for profile in aws_profiles:
        security_groups = get_security_groups(profile)
        write_to_csv(security_groups, profile)
    
    # Tüm CSV dosyalarını birleştir
    merge_csv_files()

if __name__ == "__main__":
    main()
