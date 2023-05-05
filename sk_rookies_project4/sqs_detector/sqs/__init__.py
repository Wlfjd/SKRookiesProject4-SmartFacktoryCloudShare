import boto3
import time
import json


def receive_message():
    DEFAULT_MESSAGE = 'No Message'

    sqs = boto3.client('sqs', region_name='us-west-2')
    q_name = 'https://sqs.us-west-2.amazonaws.com/792797522079/s3_upload_from_agent'
    
    res = sqs.receive_message(
        QueueUrl=q_name,
        AttributeNames=[
            'SentTimestamp'
            ],
        MessageAttributeNames=[
            'string',
            ],
        MaxNumberOfMessages=1,
        VisibilityTimeout=1,
        WaitTimeSeconds=1,
    )

    try :
        body = res['Messages'][0]['Body']
        file_name = json.loads(body)['requestPayload']['Records'][0]['s3']['object']['key'] if body != DEFAULT_MESSAGE else None
    
        if body != DEFAULT_MESSAGE:
            receipt_handle = res['Messages'][0]['ReceiptHandle']
            body = res['Messages'][0]['Body']
            body = json.dumps(body)
            print(f'{file_name} 이미지가 도착했습니다')
    
            sqs.delete_message(
                QueueUrl=q_name,
                ReceiptHandle=receipt_handle
            )
            
        return file_name
        
    except Exception as e :
        print(e)
        return None
        
    