import requests
from oci.signer import Signer
import os
import json

DIR = os.path.dirname(os.path.abspath(__file__))
PAYLOAD_FILE = f"{DIR}/payload.json"
KEY_FILE = f"/tmp/key.pem"

KEY = os.environ.get("KEY").replace("\\n", "\n")
KEY_FINGERPRINT = os.environ.get("FINGERPRINT")
TENACY = os.environ.get("TENACY")
USER = os.environ.get("USER")

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT")

MEMORY_PER_CPU = 6
DONE_CODE = "Out of host capacity."

TELEGRAM_MESSAGE = (
    "*OCI\\-Cron Function got a different response:*\n" "```json\n" "{}\n```"
)
NO_NOTIF_CODES = ["LimitExceeded", "InternalError", "TooManyRequests"]


def fill_payload(cfg):
    cfg["metadata"]["ssh_authorized_keys"] = os.environ.get("VM_SSH")
    cfg["compartmentId"] = os.environ.get("VM_COMPARTMENT")
    cfg["displayName"] = os.environ.get("VM_NAME")
    cfg["availabilityDomain"] = os.environ.get("VM_DOMAIN")
    cfg["sourceDetails"]["imageId"] = os.environ.get("VM_BOOT_IMAGE")
    cfg["sourceDetails"]["bootVolumeSizeInGBs"] = int(
        os.environ.get("VM_BOOT_VOL_SIZE")
    )
    cfg["createVnicDetails"]["subnetId"] = os.environ.get("VM_SUBNET")
    cpu = int(os.environ.get("VM_CPU_COUNT"))
    cfg["shapeConfig"]["ocpus"] = cpu
    cfg["shapeConfig"]["memoryInGBs"] = cpu * MEMORY_PER_CPU


def notify(response):
    if (
        response.code != 200
        or TELEGRAM_TOKEN is None
        or response.json().get("code") in NO_NOTIF_CODES
    ):
        return

    print("Got different response, notifying...")
    res = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": TELEGRAM_MESSAGE.format(response.text),
            "parse_mode": "MarkdownV2",
        },
    )
    print("Notification result: ", res.json())


def handler(event, context):
    print("Starting...")
    with open(KEY_FILE, "w") as f:
        f.write(KEY)

    signer = Signer(TENACY, USER, KEY_FINGERPRINT, KEY_FILE)

    with open(PAYLOAD_FILE, "r") as f:
        payload = json.load(f)

    fill_payload(payload)
    print("Got payload & key")

    response = requests.post(
        "https://iaas.sa-saopaulo-1.oraclecloud.com/20160918/instances/",
        auth=signer,
        json=payload,
    )

    print(f"Response: {response.json()}")
    notify(response)

    return {"statusCode": 200, "body": response.text}
