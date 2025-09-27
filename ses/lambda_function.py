import os
from datetime import datetime, timezone
from utils import download_github_repo, save_file_to_s3, send_email, generate_response

S3_BUCKET = os.getenv('S3_BUCKET')
SES_SENDER_EMAIL = os.getenv('SES_SENDER_EMAIL')
SES_RECIPIENTS = os.getenv('SES_RECIPIENTS')
GITHUB_REPO = os.environ.get('GITHUB_REPO')
BRANCH = os.environ.get('BRANCH', 'main')

def lambda_handler(event, context):
    try:
        github_url = f'https://github.com/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip'
        file_data = download_github_repo(github_url)
        todays_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        s3_key = f'{todays_date}/{GITHUB_REPO.replace('/', '_')}_{BRANCH}.zip'
        s3_backup_file_link = save_file_to_s3(S3_BUCKET, s3_key, file_data)
        email_body = 'GitHub backup has been successfully completed. The backup file is saved to s3.' + '\n' + f'Backup file link: {s3_backup_file_link}'
        send_email(SES_SENDER_EMAIL, SES_RECIPIENTS, 'GitHub Backup Completed', email_body)
        return generate_response(200, 'message', 'GitHub Backup successfully completed. Email is sent to the recipients.')
    except Exception as e:
        print(f'Backup failed: {e}')
        email_body = 'GitHub backup task failed. Please check AWS logs for more details.'
        send_email(SES_SENDER_EMAIL, SES_RECIPIENTS, 'GitHub Backup Failed', email_body)
        return generate_response(500, 'error', email_body)
