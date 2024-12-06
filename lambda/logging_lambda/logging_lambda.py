import json
import boto3
import time

def lambda_handler(event, context):
    log_client = boto3.client('logs')
    log_group_name = '/aws/lambda/s3_operation_logs'
    log_stream_name = 's3_operations'

    # Ensure log stream is created
    try:
        log_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except log_client.exceptions.ResourceAlreadyExistsException:
        pass  # Log stream already exists

    # Log the incoming event for debug purposes
    print("Received event:", json.dumps(event))

    processed_records = []

    for record in event['Records']:
        print("Record Body:", record['body'])
        body = json.loads(record['body'])
        print("Decoded Body:", body)

        if 'Message' in body:
            try:
                sns_message = json.loads(body['Message'])
                print("SNS Message:", sns_message)

                if 'Records' in sns_message:
                    for s3_event in sns_message['Records']:
                        object_key = s3_event['s3']['object']['key']
                        bucket_name = s3_event['s3']['bucket']['name']
                        event_name = s3_event['eventName']
                        size_delta = s3_event['s3']['object'].get('size', 0)
                        if 'ObjectRemoved' in event_name:
                            size_delta = -size_delta  # Change sign for deletions

                        log_event = {
                            'timestamp': int(time.time() * 1000),  # CloudWatch needs milliseconds
                            'message': json.dumps({
                                'object_name': object_key,
                                'size_delta': size_delta
                            })
                        }

                        # Send log event to CloudWatch
                        log_client.put_log_events(
                            logGroupName=log_group_name,
                            logStreamName=log_stream_name,
                            logEvents=[log_event]
                        )

                        processed_records.append({
                            'object_key': object_key,
                            'size_delta': size_delta,
                            'event_name': event_name
                        })
                else:
                    print("No 'Records' key in SNS Message, may not be an S3 event notification.")
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)

    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Successfully processed S3 event logs.',
            'processed_records': processed_records
        })
    }

    print("Response:", json.dumps(response))
    return response
