# AWS Lambda Function - Cron triggered Oracle Ampere VM creation

# Build

`docker build -t oci-cron .`

# Run locally

Add the `KEY` environment variable to the file `.env`. On two separate consoles, run:
`docker run --env-file .env -p 9000:8080 oci-cron`
`curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

# Push to repo

1. `docker tag oci-cron 670394663789.dkr.ecr.sa-east-1.amazonaws.com/oci-cron:{VERSION HERE}`
2. `docker push 670394663789.dkr.ecr.sa-east-1.amazonaws.com/oci-cron:{VERSION HERE}`

# Deploying

- Deploy the image from the repo and increase the memory, or else the function will time out.
- Add `EventBridge (CloudWatch Events)` trigger to run every 5m
