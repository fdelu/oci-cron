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

MEMORY_PER_CPU = 6


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
    ).json()

    print(f"Response: {response}")
    return {"statusCode": 200, "body": json.dumps(response)}
