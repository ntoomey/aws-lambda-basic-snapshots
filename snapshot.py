# Script to take a snapshot of EBS volumes to be used with Lambda as 
# as a scheduled task

import boto3
import datetime
# region
region = "us-east-1"
# day
day = datetime.date.strftime(datetime.datetime.now(),"%x") 
# volume filter
filter = [{'Name': "tag:Snapshot",'Values': ["True"]}]
# boto3 client
client = boto3.client("ec2", region)

def get_volume_name(tags):
        for t in tags:
            if t['Key'] == 'Name':
                v = t['Value'] 
                break 
            else:
                v = ""
        return v


def snapshot_volumes( volumes, description ):
    for volume in volumes['Volumes']:
        volumeid = volume['VolumeId']

        # create snapshot of volume
        snap = client.create_snapshot(VolumeId=volumeid,Description=description)

        # get the name of the original volume and pass it on to the snapshot
        volume_name = get_volume_name(volume['Tags'])
        if volume_name:
            client.create_tags(Resources=[snap['SnapshotId']],Tags=[{'Key': 'Name','Value': volume_name}])

# get voumes
volumes = client.describe_volumes(Filters=filter)
# create snapshots
snapshot_volumes(volumes, day)
