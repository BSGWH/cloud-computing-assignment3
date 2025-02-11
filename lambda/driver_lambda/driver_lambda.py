import boto3
import time
import requests
import os

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = 'weihao-cdk-bucket'
    PLOTTING_API_URL = os.getenv('PLOTTING_API_URL')

    # Create assignment1.txt
    s3_client.put_object(
        Bucket=bucket_name, 
        Key='assignment1.txt', 
        Body='Empty Assignment 1'
    )
    print("Created assignment1.txt")
    time.sleep(5)  # Add some delay

    # Create assignment2.txt
    s3_client.put_object(
        Bucket=bucket_name, 
        Key='assignment2.txt', 
        Body='Empty Assignment 2222222222'
    )
    print("Created assignment2.txt")
    time.sleep(5)  # Add some delay

    # Create assignment3.txt
    s3_client.put_object(
        Bucket=bucket_name, 
        Key='assignment3.txt', 
        Body='33'
    )
    print("Created assignment3.txt")
    time.sleep(5)  # Add some delay

    # Call plotting lambda API (replace with actual API endpoint)
    try:
        response = requests.get(PLOTTING_API_URL)
    except Exception as e:
        print(f"Error calling plotting lambda: {e}")

    return {
        'statusCode': 200,
        'body': 'Objects created and API called'
    }