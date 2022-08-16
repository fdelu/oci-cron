# AWS Lambda Function - Cron triggered Oracle Ampere VM creation

Uses Oracle Cloud REST API to create an Ampere instance. The instances are usually out of stock, so this was created in order to run every minute on an AWS Lambda Function until it succeeds.

Once the instance it created, the user is notified via Telegram.

> The code is set up for accounts in Sao Paulo. Change the POST_URL constant if needed.

# Build

`docker build -t oci-cron .`

# Environment variables

You can get most of this values by attempting to create an instance manually and looking into the payload of the packet that is sent.

- `KEY`: Oracle cloud API Key file content. Replace new lines with the literal `\n`
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
- `TELEGRAM_TOKEN`: (optional) Telegram bot token to send a notification when done.
- `TELEGRAM_CHAT`: (optional) Telegram chat id where the notification is sent.

> In order to get a notification, you must have started a chat with the bot before.

> You can get your Telegram's chat id by sending a message to the bot `@userinfobot`.

# Run locally

Add the environment variables to a file named `.env`.

On two separate terminals, run:

- `docker run --env-file .env -p 9000:8080 oci-cron`
- `curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`

# Pushing to AWS repository

Use this commands to push to an AWS repository in order to deploy the function

- `docker tag oci-cron {REPO_URL}:{VERSION HERE}`
- `docker push {REPO_URL}:{VERSION HERE}`

# Deploying

- Deploy the image from the repository
- Increase the memory (tested with 1GB), or else the function will time out.
- Add an `EventBridge (CloudWatch Events)` trigger to run every minute
