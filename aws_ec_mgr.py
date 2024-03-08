""" helper to start and stop ec2 instances """
import argparse
import sys
import time
import boto3
from wa_hack_cli import simple_send

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start or stop ec2 instances')
    parser.add_argument('-a', '--action', help='start or stop')
    parser.add_argument('-r', '--region', help='region')
    parser.add_argument('-i', '--instance_id', help='instance id')
    args = parser.parse_args()
    action = args.action
    region = args.region
    instance_id = args.instance_id

    WA_SRV = '192.168.123.38'
    WA_PORT = 9009
    WA_DESTINATION = '491717626871'
    WA_MESSAGE = f'*AWS Status Overview* - {time.strftime("%d.%m.%Y %H:%M")}\n'

    ec2 = boto3.resource('ec2', region_name=region)

    if action == 'start':
        ec2.instances.filter(InstanceIds=[instance_id]).start()
        print('starting instance', instance_id)
    elif action == 'stop':
        ec2.instances.filter(InstanceIds=[instance_id]).stop()
        print('stopping instance', instance_id)
    elif action in ['status', 'state']:
        instance = ec2.Instance(instance_id)
        print(instance.state['Name'])
    elif action == 'list':
        instances = ec2.instances.all()
        for i in instances:
            WA_MESSAGE = f"{WA_MESSAGE}{i.id} {i.state['Name']} {i.public_ip_address}\n"
        # print(WA_MESSAGE)
        simple_send(WA_SRV, WA_PORT, WA_DESTINATION, WA_MESSAGE)

    elif action == 'public_ip':
        instance = ec2.Instance(instance_id)
        print(instance.public_ip_address)
    elif action == 'private_ip':
        instance = ec2.Instance(instance_id)
        print(instance.private_ip_address)
    elif action == 'public_dns':
        instance = ec2.Instance(instance_id)
        print(instance.public_dns_name)
    elif action == 'status_all':
        instances = ec2.instances.all()
        for i in instances:
            print(i.id, i.state['Name'], i.public_ip_address)
    else:
        print('invalid action')
        sys.exit(1)