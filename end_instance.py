import boto3
import time
from core import get_spot_instance, save_image_instance

ec2 = boto3.client('ec2')
spot_instance = get_spot_instance()

print("Saving image")
save_reponse = save_image_instance(spot_instance['InstanceId'])
time.sleep(60)
print()


### Clearing snapshots
print("Deleting useless snapshots")
snapshots = ec2.describe_snapshots(OwnerIds=['233890315439'])
snapshots_sorted = sorted(snapshots['Snapshots'], key = lambda d: d['StartTime'])

if len(snapshots_sorted) > 1:
    snapshots_to_delete = [d['SnapshotId'] for d in snapshots_sorted[-1]]

for snapshot_id in snapshots_to_delete:
    ec2.delete_snapshot(SnapshotId=snapshot_id)
################################################################################

print("Cancelling spot request")
cancel_response = ec2.cancel_spot_instance_requests(
    SpotInstanceRequestIds=[spot_instance['SpotInstanceRequestId']])

print(cancel_response['CancelledSpotInstanceRequests'])

print("Shutting down instances")
terminate_response = ec2.terminate_instances(InstanceIds=[spot_instance['InstanceId']])
print(terminate_response['TerminatingInstances'])

# End spot request
