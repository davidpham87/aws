import boto3
import time
from core import get_spot_instance, save_image_instance

ec2 = boto3.client('ec2')
spot_instance = get_spot_instance()

print("Saving image")
save_reponse = save_image_instance(spot_instance['InstanceId'])
time.sleep(300)
print()

print("Cancelling spot request")

cancel_response = ec2.cancel_spot_instance_requests(
    SpotInstanceRequestIds=[spot_instance['SpotInstanceRequestId']])

print(cancel_response['CancelledSpotInstanceRequests'])

print("Shutting down instances")

terminate_response = ec2.terminate_instances(InstanceIds=[spot_instance['InstanceId']])

print(terminate_response['TerminatingInstances'])

# End spot request
