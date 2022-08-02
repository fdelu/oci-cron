import requests
from oci.signer import Signer
import os
import json

DIR = os.path.dirname(os.path.abspath(__file__))

PAYLOAD_FILE =  f"{DIR}/payload.json"
KEY_FILE = f"/tmp/key.pem"
KEY = os.environ.get("KEY").replace("\\n", "\n")
KEY_FINGERPRINT = "af:1f:c4:da:34:ff:22:02:30:fc:97:f3:20:5a:2f:2d"
TENACY = "ocid1.tenancy.oc1..aaaaaaaaozrv4ilyferxbg2rdek5klfdewdy6tlkocwtbpnpkmrk2j6pz5tq"  # noqa
REGION = "sa-saopaulo-1"
USER = "ocid1.user.oc1..aaaaaaaays2rpdcslmlqcbofop2qf77r4a4zs2xyhykzijpic6y2byc7qwfa"


def handler(event, context):
    print("Starting...")
    with open(KEY_FILE, "w") as f:
        f.write(KEY)

    signer = Signer(TENACY, USER, KEY_FINGERPRINT, KEY_FILE)

    with open(PAYLOAD_FILE, "r") as f:
        payload = json.load(f)

    print("Got payload & key")

    response = requests.post(
        "https://iaas.sa-saopaulo-1.oraclecloud.com/20160918/instances/",
        auth=signer,
        json=payload,
    ).json()

    print(f"Response: {response}")
    return {"statusCode": 200, "body": json.dumps(response)}
