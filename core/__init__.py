import boto3
import itertools as it

def get_spot_instance():
    ec2 = boto3.client('ec2')

    # make a request
    response = ec2.describe_instances()
    instances = [d['Instances'] for d in response['Reservations']]
    instances = list(it.chain.from_iterable(instances))
    instances = [d for d in instances if d['State'].get('Code', 48) != 48]
    instances = [d for d in instances if d['InstanceLifecycle'] == 'spot']

    spot_instance = {}
    if len(instances) == 1:
        spot_instance = instances[0]
    return spot_instance

def get_image_id(ami_name = 'ubuntu_machine_learning'):
    ec2 = boto3.client('ec2')
    images = ec2.describe_images(
        Filters=[{'Name': 'name', 'Values' : [ami_name]}])
    image_id = 'ami-ceb39fab'
    if images.get('Images', []):
        image_id =  images['Images'][0]['ImageId']
    return image_id


def save_image_instance(instance_id, ami_name='ubuntu_machine_learning'):
    ec2 = boto3.client('ec2')
    image_id = get_image_id(ami_name)
    if image_id:
        try:
            ec2.deregister_image(ImageId=image_id)
        except:
            pass
    response = ec2.create_image(
        InstanceId=instance_id,
        Name=ami_name)
    return response
