import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Users
table = dynamodb.create_table(
    TableName='Climate',
    KeySchema=[
        {'AttributeName': 'user_id', 'KeyType': 'HASH'}  # Partition key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'user_id', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait for table to be created
table.meta.client.get_waiter('table_exists').wait(TableName='Users')

print(f"Table status: {table.table_status}")
