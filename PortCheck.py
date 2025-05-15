import boto3
import csv

# Ports to check
REQUIRED_PORTS = [80, 443]

def get_open_ports(ip_permissions):
    open_ports = set()
    for rule in ip_permissions:
        from_port = rule.get('FromPort')
        to_port = rule.get('ToPort')
        if from_port is not None and to_port is not None:
            for port in range(from_port, to_port + 1):
                open_ports.add(port)
    return open_ports

def main():
    ec2 = boto3.client('ec2')
    # Include both running and stopped instances
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]
    )

    report_data = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            public_ip = instance.get('PublicIpAddress', 'N/A')
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            name_tag = next(
                (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A'
            )
            sg_ids = [sg['GroupId'] for sg in instance['SecurityGroups']]
            open_ports = set()

            for sg_id in sg_ids:
                sg = ec2.describe_security_groups(GroupIds=[sg_id])['SecurityGroups'][0]
                open_ports.update(get_open_ports(sg['IpPermissions']))

            missing_ports = [port for port in REQUIRED_PORTS if port not in open_ports]
            ports_status = "All Open" if not missing_ports else f"Missing {missing_ports}"

            report_data.append({
                'Instance ID': instance_id,
                'Name': name_tag,
                'State': state,
                'Public IP': public_ip,
                'Private IP': private_ip,
                'Security Groups': ', '.join(sg_ids),
                'Port 80': 'Open' if 80 in open_ports else 'Closed',
                'Port 443': 'Open' if 443 in open_ports else 'Closed',
                'Status': ports_status
            })

    # Write to CSV
    csv_file = 'ec2_port_check_report.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
        writer.writeheader()
        writer.writerows(report_data)

    print(f"✅ Report generated: {csv_file}")

if __name__ == '__main__':
    main()
