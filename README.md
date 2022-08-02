# AWS Lambda Function - Cron triggered Oracle Ampere VM creation

# Build

`docker build -t oci-cron .`

# Environment variables

- `KEY`: Oracle cloud API Key file content, replacing new lines with `\n`
- `KEY_FINGERPRINT`: Oracle cloud API Key fingerprint
- `TENACY`: Oracle cloud tenacy
- `USER`: Oracle cloud user
- `VM_NAME`: Name of the created instance
- `VM_SSH`: Authorized key for access to the instance
- `VM_BOOT_IMAGE`: Boot image ID
- `VM_BOOT_VOL_SIZE`: Boot volume size. Free tier allos up to 200gb shared between all instances.
- `VM_SUBNET`: Subnet ID
- `VM_COMPARTMENT`: Compartment ID
- `VM_DOMAIN`: Availability Domain ID
- `VM_CPU_COUNT`: Amount of CPUs. Memory will be 6 times this amount.

# Run locally

Add the `KEY` environment variable to the file `.env`.

On two separate consoles, run:

- `docker run --env-file .env -p 9000:8080 oci-cron`
- `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

# Push to repo

- `docker tag oci-cron 670394663789.dkr.ecr.sa-east-1.amazonaws.com/oci-cron:{VERSION HERE}`
- `docker push 670394663789.dkr.ecr.sa-east-1.amazonaws.com/oci-cron:{VERSION HERE}`

# Deploying

- Deploy the image from the repo and increase the memory, or else the function will time out.
- Add `EventBridge (CloudWatch Events)` trigger to run every 5m
