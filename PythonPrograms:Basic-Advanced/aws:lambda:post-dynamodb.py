import json
import boto3

def create_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'UserId',
            'AttributeType': 'S'
        },
    ],
    TableName='UserDetails',
    KeySchema=[
        {
            'AttributeName': 'UserId',
            'KeyType': 'HASH'
        },
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    )
    
    table.meta.client.get_waiter('table_exists').wait(TableName='UserDetails')
    print("Table status:", table.table_status)


def perform_put(data):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('UserDetails')
    
    table.put_item(
        Item = {
            "UserId": data['UserId'],
            "Age": data['Age'],
            "Height": data['Height'],
            "Income": data['Income']
        }
        )
    print(f'Added values !!!')


def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    try:
        response = client.describe_table(TableName='UserDetails')
        perform_put(event)
    except client.exceptions.ResourceNotFoundException:
        create_table()
        perform_put(event)

    
