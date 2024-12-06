import json
import boto3
import time

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cdk-S3-object-size-history')

    print("Received event: " + json.dumps(event))
    # Process each message from SQS
    for record in event['Records']:
        message_body = json.loads(record['body'])
        s3_event = message_body['Records'][0]  # This depends on the structure of the message stored in SQS
        bucket_name = s3_event['s3']['bucket']['name']
        object_key = s3_event['s3']['object']['key']
        
        print(f"Processing object {object_key} in bucket {bucket_name}")  # Log the object being processed
        # Assuming each message contains info about a single object modification
        object_key = s3_event['s3']['object']['key']
        
        # Calculate total size and object count of the bucket
        try:
            response = s3.list_objects_v2(Bucket=bucket_name)
            total_size = sum(obj['Size'] for obj in response.get('Contents', []))
            object_count = response['KeyCount']
        except Exception as e:
            print(f"Error calculating bucket size: {str(e)}")
            continue  # Skip to the next record if there's an error

        # Write the computed data to DynamoDB
        try:
            table.put_item(
                Item={
                    'bucket_name': bucket_name,
                    'timestamp': str(int(time.time())),
                    'total_size': total_size,
                    'object_count': object_count
                }
            )
        except Exception as e:
            print(f"Error writing to DynamoDB: {str(e)}")
