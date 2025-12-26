import base64
import json
from datetime import datetime
from google.cloud import firestore

db = firestore.Client()

COLLECTION_NAME = "pubsub_events"


def pubsub_to_firestore(cloud_event):
   

    try:
        message = cloud_event.data["message"]
        data = base64.b64decode(message["data"]).decode("utf-8")
        payload = json.loads(data)

        doc = {
            "user": payload.get("user"),
            "event": payload.get("event"),
            "received_at": datetime.utcnow()
        }

        db.collection(COLLECTION_NAME).add(doc)

        print(" Data inserted into Firestore:", doc)

    except Exception as e:
        print(" Error processing message:", str(e))
