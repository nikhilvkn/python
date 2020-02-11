# This program helps to add multiple tags for ec2 instance

import pandas as pd
import logging
import boto3

AWS_PROFILE='xxxx'
AWS_REGION='xxxx'

def gatherinstanceid():
    ''' function to gather instance id '''
    
    instanceid = []  
    response = client.describe_instances()
    
    for contents in response['Reservations']:
        for values in contents['Instances']:
            instanceid.append(values['InstanceId'])
     
    return instanceid

def createtag(count,instance):
    ''' function to create tags for given instance '''
    
    client.create_tags(
        Resources=[instance],
        Tags=[
            {
                'Key': 'Name',
                'Value':dataframe['Name'].values[count]
            },
            {   'Key': 'Service',
                'Value': dataframe['Service'].values[count]
            },
            {  'Key': 'Owner',
                'Value': dataframe['Owner'].values[count]
            },
            {   'Key': 'Env',
                'Value': dataframe['Env'].values[count]
            },
        ]
    )

if __name__ == '__main__':
    ''' AWS tag program '''
    
    try:
        boto3.setup_default_session(profile_name=AWS_PROFILE,region_name=AWS_REGION)
        client = boto3.client('ec2')
        dataframe = pd.read_excel('techopstest-tag.xlsx')
        logging.basicConfig(
            level=logging.INFO, 
            filename='ec2instance-tag.log', 
            filemode='w', 
            format='%(name)s - %(levelname)s - %(message)s'
        )

        instanceid = gatherinstanceid()  
        count = 0
        for instance in dataframe['InstanceID']:
            logging.info('Updating {}'.format(instance))
            createtag(count,instance)
            count += 1
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception("Exception occurred")
    finally:
        logging.info('\n Completed Execution \n')

