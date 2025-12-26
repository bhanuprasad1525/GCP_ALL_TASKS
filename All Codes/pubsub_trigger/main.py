import base64
import json
from datetime import datetime

def pubsub_msg(cloud_event):
 
    message = cloud_event.data["message"]
    data = base64.b64decode(message["data"]).decode("utf-8")
    payload = json.loads(data)

    user = payload.get("user")
    event = payload.get("event")

    print("Pub/Sub message received")
    print("User:", user)
    print("Event:", event)
    print("Received at:", datetime.utcnow())
