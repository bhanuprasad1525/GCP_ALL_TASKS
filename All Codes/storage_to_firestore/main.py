import json
from datetime import datetime
from google.cloud import storage
from google.cloud import firestore

storage_client = storage.Client()
firestore_client = firestore.Client()

COLLECTION_NAME = "uploaded_files"


def gcs_to_firestore(cloud_event):
   

    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"File uploaded: {file_name} in bucket {bucket_name}")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_content = blob.download_as_text()

 
    records = json.loads(file_content)

 
    if isinstance(records, list):
        for record in records:
            record["processed_at"] = datetime.utcnow()
            firestore_client.collection(COLLECTION_NAME).add(record)


    else:
        records["processed_at"] = datetime.utcnow()
        firestore_client.collection(COLLECTION_NAME).add(records)

    print("Data successfully loaded into Firestore")
