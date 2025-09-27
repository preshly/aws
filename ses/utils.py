import boto3
import json
import urllib.request

AWS_REGION = 'ap-south-1'

def download_github_repo(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return response.read()
    except Exception as e:
        print(f'Error downloading the file: {e}')
        raise


def save_file_to_s3(s3_bucket: str, s3_key: str, file_data: bytes) -> str:
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=file_data)
        return f'https://s3.console.aws.amazon.com/s3/object/{s3_bucket}/{s3_key}?region={AWS_REGION}'
    except Exception as e:
        print(f'Error uploading the file to s3: {e}')
        raise


def send_email(sender_email: str, ses_recipients: str, subject: str, body: str) -> None:
    if ses_recipients is None or ses_recipients.strip() == '':
        return
    recipient_emails = [r.strip() for r in ses_recipients.split(',')]
    ses_client = boto3.client('ses', region_name=AWS_REGION)
    try:
        ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': recipient_emails
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
    except Exception as e:
        print(f'Error sending email: {e}')
        raise


def generate_response(status_code: int, response_body_key: str, response_messgae: str):
    return {
        'statusCode': status_code,
        'body': json.dumps({response_body_key: response_messgae})
    }
