»import boto3
import time
from core import get_spot_instance, get_image_id

spot_price = '0.02'
instance_type = "c4.large"

launch_specs = {
    "ImageId": get_image_id('ubuntu_machine_learning'),
    "InstanceType": instance_type,
    "KeyName": "linux-key",
    "BlockDeviceMappings": [ {
        "DeviceName": "/dev/sda1",
        "Ebs": { "DeleteOnTermination": True,
                 "VolumeType": "gp2", "VolumeSize": 50}}]}

ec2 = boto3.client('ec2')

response = ec2.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification=launch_specs,
    SpotPrice=spot_price, Type="one-time")

print("Creating spot instance")
spot_instance = get_spot_instance()

k, n_trials = 0, 10
print("Requesting spot instance")
while not spot_instance and k <= n_trials:
    time.sleep(1)
    spot_instance = get_spot_instance()
    k += 1

if not spot_instance:
    raise RuntimeError('Not spot instance available')

print("Spot instance created")
ip_address = spot_instance['PublicDnsName']
ssh_address = "ubuntu@{}".format(ip_address)
ssh_command = 'ssh -i "~/.ssh/linux-key.pem" '

print("IP Adress : {}".format(ssh_address))
print("Connect via")
print(ssh_command + ssh_address)

launch_jupyter = ' '.join([
    ssh_command, ssh_address, 'jupyter notebook --port=8888'])

with open('launch_jupyter.sh', 'w') as f:
    f.write(launch_jupyter + '\n')
print(launch_jupyter)

ssh_jupyter = 'ssh -i "~/.ssh/linux-key.pem" -L 8000:localhost:8888 ' + \
             ssh_address
with open('ssh_connection.sh', 'w') as f:
    f.write(ssh_jupyter + '\n')

print('Connect to it')
print(ssh_jupyter)
