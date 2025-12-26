import base64
import json
from datetime import datetime
from google.cloud import bigquery

bq_client = bigquery.Client()
TABLE_ID = "bhanu project 1.user_analytics.user_events"

def pubsub_to_bigquery(cloud_event):
  
    message = cloud_event.data["message"]
    data = base64.b64decode(message["data"]).decode("utf-8")
    payload = json.loads(data)

    row = {
        "event_name": payload.get("event"),
        "user_name": payload.get("user"),
        "event_time": datetime.utcnow().isoformat()
    }

    errors = bq_client.insert_rows_json(TABLE_ID, [row])

    if errors:
        print(" BigQuery insert errors:", errors)
    else:
        print(" Data inserted into BigQuery:", row)
