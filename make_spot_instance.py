import boto3
import time
import storm # ssh
from core import get_spot_instance, get_image_id

CREATE_REQUEST = True
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

if CREATE_REQUEST:
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
k, ip_address = 0, ''
while not ip_address and k < n_trials:
    k += 1
    ip_address = spot_instance['PublicDnsName']
    time.sleep(1)

if not ip_address:
    raise RuntimeError('Not spot instance available')


ssh_config = storm.Storm()

if not ssh_config.is_host_in('aws'):
    ssh_config.add_entry(
        'aws', ip_address, 'ubuntu', 22, '~/.ssh/linux-key.pem')
else:
    ssh_config.update_entry('aws', hostname=ip_address)

if not ssh_config.is_host_in('aws-jupyter'):
    ssh_config.add_entry(
        'aws-jupyter', ip_address, 'ubuntu',
        22,  '~/.ssh/linux-key.pem',
        [('localforward', '8000 localhost:8888')])
else:
    ssh_config.update_entry('aws-jupyter', hostname=ip_address,
                            localforward='8000 localhost:8888')

print("Connect via")
print('ssh aws')

launch_jupyter = ' '.join([
    'ssh aws "jupyter notebook --port=8888"'])

print('''Connect to it:
ssh aws-jupyter
Enter this in a browser:
https://{}:8888/
Or alternatively
https://localhost:8000/'''.format(ip_address))




