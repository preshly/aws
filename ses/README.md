# Backup Notification Stack using SES

This template provisions an **AWS Lambda** function for backup task execution and integrates **AWS SES** for user notifications.

It creates:

- **Lambda** function to download a GitHub repository archive.
- Stores it in a **S3** bucket.
- Sends a notification email via **Amazon SES**.

## Prerequisites

1. **AWS CLI** installed and configured with proper credentials and region.
2. **SES** verified email addresses (for sender and recipients).

## Template Parameters

- **GitHubRepo**: The GitHub repo to backup (e.g., owner/repo).
- **GitHubBranch**: The branch to back up (e.g., main).
- **S3Bucket**: The S3 bucket where backups will be stored.
- **SesSenderEmail**: Verified SES email to send notifications.
- **SesRecipients**: Comma-separated SES verified recipient emails.

## Prepare Deployment Package

Zip the Lambda function code before deploying:

```bash
Compress-Archive \* publish.zip
```

## Deploy the Stack

**Note**: You need to create a S3 bucket to publish the code package files.

To deploy the backup-notification stack:

```bash
aws cloudformation package --template-file template.yaml --s3-bucket <s3-bucket-for-deployments> --s3-prefix BackupNotificationService --output-template-file package.yaml

aws cloudformation deploy --template-file package.yaml --stack-name backup-notification --capabilities CAPABILITY_NAMED_IAM --parameter-overrides GitHubRepo=<owner/repo> GitHubBranch=main S3Bucket=<s3-bucket> SesSenderEmail=<your-ses-verified-email@example.com> SesRecipients=<recipient1@example.com,recipient2@example.com>
```

## Trigger the Lambda

To invoke manually for testing:

```bash
aws lambda invoke --function-name <lambda-function-name> response.json
```

## Delete the Stack

To clean up resources:

```bash
aws cloudformation delete-stack --stack-name backup-notification
```
