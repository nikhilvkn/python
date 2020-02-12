import sys
import csv
import boto3
from multiprocessing import Pool

DRY_RUN = False 

INPUT_FILE = "input-files/env-classification.csv"
AWS_REGIONS = [ "us-east-1", "us-east-2", "us-west-1", "us-west-2" ]

CPU_CORES = 8

req_tags = [
]

TAG_DATA = dict()
ec2clients = dict()

for region in AWS_REGIONS:
    ec2clients[region] = boto3.client("ec2",region_name=region)
    

def get_tag_data():
    
    file_reader = csv.DictReader(open(INPUT_FILE))
    for row in file_reader:
        instance_id = row.get("InstanceId").strip()
        ch_env = row.get("CloudHealthEnv").strip()
        ch_service_env = row.get("CloudHealthServiceEnv").strip()
        if ch_env.rfind("/") >= 0:
            ch_env = ch_env.replace("/", "-", -1)
        if ch_service_env.rfind("/") >= 0:
            ch_service_env = ch_service_env.replace("/", "-", -1)
        TAG_DATA[instance_id] = { "CloudHealthEnv" : ch_env, "CloudHealthServiceEnv" : ch_service_env }

def get_instances(region):

    instance_data = list()

    ec2client =  ec2clients.get(region)
    _ins_data = ec2client.describe_instances()

    for res in _ins_data.get("Reservations"):
        for ins in res.get("Instances"):
            instance_id = ins.get("InstanceId")
            instance_data.append({ "InstanceId" : instance_id, "Region" : region })

    return instance_data


def add_tags(ins_data):
    
    instance_id = ins_data.get("InstanceId")
    region = ins_data.get("Region")
    if instance_id in TAG_DATA:
        ch_env = TAG_DATA[instance_id].get("CloudHealthEnv")
        ch_service_env = TAG_DATA[instance_id].get("CloudHealthServiceEnv")
        ec2client = ec2clients.get(region) 

        
        if DRY_RUN:
            print("Adding tags for %s: %s, %s" % (instance_id, ch_env, ch_service_env))
            return instance_id
        else:
            ec2client.create_tags( DryRun=DRY_RUN,
                        Resources=[instance_id],
                        Tags=[
                                { 
                                    'Key'   :   'CloudHealthEnv',
                                    'Value' :   ch_env
                                },
                                {
                                    'Key'   :   'CloudHealthServiceEnv',
                                    'Value' :   ch_service_env
                                }]
            )
    else:
        print("Instance tag information not available: %s" % instance_id)

    return instance_id

def main():
    
    all_ins = list()

    get_tag_data()
    pool = Pool(processes=CPU_CORES)

    for _ins_data in pool.imap_unordered(get_instances, AWS_REGIONS):
        all_ins.extend(_ins_data)

    tags_added_list = list()
    for instance_id in pool.imap_unordered(add_tags, all_ins):
        tags_added_list.append(instance_id)

if __name__ == '__main__':
    main()
