""" helper to start and stop ec2 instances """
import argparse
import sys
import time
import boto3

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start or stop ec2 instances')
    parser.add_argument('-a', '--action', help='start or stop')
    parser.add_argument('-r', '--region', help='region')
    parser.add_argument('-i', '--instance_id', help='instance id')
    args = parser.parse_args()
    action = args.action
    region = args.region
    instance_id = args.instance_id

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
