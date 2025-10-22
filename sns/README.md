# SNS Notification API Stack using AWS Lambda and .NET Minimal API

This stack provisions a **.NET Minimal API** running on **AWS Lambda**, integrated with **AWS SNS** for sending email notifications.

It demonstrates how you can set up lightweight APIs that trigger real-time notifications. Everything is automated with AWS CloudFormation and built using the serverless-first approach.

It creates:

- **Lambda Function** with .NET 8 Minimal API.
- **SNS Topic** for message publishing.
- ***SNS Email subscription**.
- **IAM role** for the Lambda function.
- **Lambda Function URL** for direct API testing.

## Prerequisites

1. **AWS CLI** installed and configured with proper credentials and region.
2. **.NET 8 SDK** installed on your system.
3. An **S3 bucket** to publish the code package files.

## Project Setup

1. Install `Amazon.Lambda.Tools` globally.

```bash
dotnet tool install -g Amazon.Lambda.Tools
```

2. Create a **global.json** file, to lock .NET version. Make sure you swap in the actual .NET version you have installed.

```bash
dotnet new globaljson --sdk-version 8.0.317
```

3. Install `Amazon.Lambda.Templates`.

```bash
dotnet new install Amazon.Lambda.Templates
```

4. Create a .NET project with Minimal API Lambda function.

```bash
dotnet new webapi --name SnsNotificationLambda
cd SnsNotificationLambda
```

5. Add the required NuGet packages

```bash
dotnet add package AWSSDK.Extensions.NETCore.Setup
dotnet add package AWSSDK.SimpleNotificationService
dotnet add package Amazon.Lambda.AspNetCoreServer.Hosting
```

## Template Parameters

- **SnsSubscriptionEmail**: The email address to subscribe to the SNS topic.

## Build the project

```bash
dotnet clean

dotnet build --configuration Release
```

## Prepare Deployment Package

**Note**: Before executing the below commands, ensure you are in the parent directory. This is where the CloudFormation template and the .NET project are at the same level.

```bash
dotnet lambda package -pl SnsNotificationLambda -o publish.zip
```

## Deploy the Stack

**Note**: You need to create a S3 bucket to publish the code package files.

```bash
aws cloudformation package --template-file template.yaml --s3-bucket <s3-bucket-for-deployments> --s3-prefix SnsNotificationService --output-template-file package.yaml

aws cloudformation deploy --template-file package.yaml --stack-name sns-notification --capabilities CAPABILITY_NAMED_IAM --parameter-overrides SnsSubscriptionEmail=<your-sns-subscription-email@example.com>
```

## Confirm SNS Email Subscsiption

When the deployment finishes, check the inbox of the email used to subscribe to the SNS topic for a subscription confirmation from AWS. Click the link in the email to confirm your subscription.

## Test the APIs using Postman

- Note the Lambda Function URL from CloudFormation Outputs after the stack is deployed.
- Test the endpoints.

### Health Check

```
GET <LambdaFunctionUrl>/
```

Response example:

```
Lambda health check API. System running smoothly!
```

### Get Policy Details + Send SNS Notification

```
GET <LambdaFunctionUrl>/policy
```

Response example:

```json
{
  "policyId": "POL12345",
  "holder": "John Doe",
  "premium": 5000,
  "status": "Active"
}
```

You will also receive an email notification.

## Delete the Stack

To clean up resources:

```bash
aws cloudformation delete-stack --stack-name sns-notification
```