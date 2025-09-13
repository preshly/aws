# Web Server CloudFormation Stack

This template provisions an **EC2 instance** running Apache HTTP Server with SSH and HTTP access enabled.
It creates:

- A **Security Group** allowing inbound SSH (port 22) and HTTP (port 80).
- An **EC2 instance** in a provided subnet with a public IPv4 address and Apache installed.

## Prerequisites

1. **AWS CLI** installed and configured with proper credentials and region.
2. A valid **Key Pair** already created in the AWS region.
3. A valid **Subnet ID** in the target VPC.

## Template Parameters

- **SubnetId**: The subnet where the instance will be launched.
- **KeyName**: The existing EC2 Key Pair name to allow SSH access.

## Deploy the Stack

- To deploy the simple web server:

```bash
aws cloudformation deploy --template-file web-server.yaml --stack-name web-server --capabilities CAPABILITY_NAMED_IAM --parameter-overrides SubnetId=<SubnetId> KeyName=<KeyName>
```

- To deploy the web server with network interface:

```bash
aws cloudformation deploy --template-file web-server-with-network-interface.yaml --stack-name web-server-with-network-interface --capabilities CAPABILITY_NAMED_IAM --parameter-overrides SubnetId=<SubnetId> KeyName=<KeyName>
```

## Accessing the Web Server

After deployment, find the Public IPv4 address of the instance.
Open your browser or use curl:

```bash
curl http://<public-ip-of-ec2>
```

You will see the default Apache test page.

### SSH Access

```bash
chmod 400 <my-keypair.pem>
ssh -i <my-keypair.pem> ubuntu@<public-dns-of-ec2>
```

## Delete the Stack

To clean up resources:

```bash
aws cloudformation delete-stack --stack-name web-server
```
