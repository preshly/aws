# API Gateway with AWS WAFv2 IP Blocking

This stack provisions a **REST API** in **AWS API Gateway**, protected by **AWS WAFv2** to block specific IP addresses or ranges.

It demonstrates how to quickly set up API-level security controls using WAF IP sets and Web ACLs.

It creates:
- **API Gateway REST API** with mock integration.
- **WAFv2 IP Set** for managing blocked IPs.
- **WAFv2 Web ACL** with IP blocking rule.
- **Web ACL Association** with the API Gateway stage.

## Prerequisites

1. **AWS CLI** installed and configured with proper credentials and region.
2. Your **public IP address** to test the blocking functionality.

## Get Your IP Address

Visit [https://whatismyipaddress.com/](https://whatismyipaddress.com/) to get your current public IPv4 address.

We will use this IP (in CIDR format like `203.0.113.45/32`) to test the WAF blocking.

## Template Parameters

- **ApiName**: Name of the API Gateway REST API (default: `products-api`).
- **StageName**: Deployment stage name (default: `prod`).
- **BlockedIp**: IPv4 CIDR to block (e.g., `203.0.119.5/32`).

## Deploy the Stack

```bash
aws cloudformation deploy --template-file template.yaml --stack-name api-waf --parameter-overrides BlockedIp=<YOUR_IP_ADDRESS>/32
```

Replace `<YOUR_IP_ADDRESS>` with your actual IP from [https://whatismyipaddress.com/](https://whatismyipaddress.com/).

## Test the API

Note the API Invoke URL from CloudFormation Outputs after the stack is deployed.

### Testing the API using your current IP address

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/
```

If you deployed the stack with your own IP in the `BlockedIp` parameter, the request will return:

```json
{"message":"Forbidden"}
```

### Testing Tips

**Test the block from your current location:**
- Deploy the stack with your current IP address as the `BlockedIp` parameter.
- Try accessing the API. You should be blocked.

**Test from a different location:**
- Use a VPN or different network.
- Access should work normally if the IP isn't in the block list.

**Unblock yourself:**
- Remove your IP from the IP set in the WAF console.
- Wait 30-60 seconds, then retry your request.

Response example:
```json
{
  "message": "Products API - read the docs for API usage.",
  "service": "products"
}
```

## Verify in AWS Console

- Open **AWS WAF & Shield** in the AWS Console.
- Navigate to **Protection packs (web ACLs)** under **AWS WAF** → select your Web ACL.
- Under the **Sampled requests** column, click on **View** and then click on **Dashboard**.
- You should see blocked requests with:
  - **Metric name:** BlockBadIPMetric
  - **Source IP:** Your IP address
  - **Action:** Block

## Update Blocked IPs

To add or remove IPs from the block list after deployment:

1. Go to **AWS WAF & Shield** → **IP sets** under **AWS WAF**.
2. Select the IP set created by the stack.
3. Modify the IP addresses.
4. Click **Save**.

Changes take effect within 30-60 seconds.

## Delete the Stack

To clean up resources:

```bash
aws cloudformation delete-stack --stack-name api-waf
```