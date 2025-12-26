import json
import os
from google.cloud import storage
import mysql.connector


storage_client = storage.Client()


def get_connection():
    return mysql.connector.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        unix_socket=os.environ["DB_SOCKET"]  
    )


def gcs_to_cloudsql(cloud_event):
  

    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"File uploaded: {file_name}")

   
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_content = blob.download_as_text()

    records = json.loads(file_content)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO users (user_name, event_name)
        VALUES (%s, %s)
    """

    if isinstance(records, list):
        for record in records:
            cursor.execute(
                insert_query,
                (record.get("user"), record.get("event"))
            )
    else:
        cursor.execute(
            insert_query,
            (records.get("user"), records.get("event"))
        )

    conn.commit()
    cursor.close()
    conn.close()

    print("Data successfully inserted into Cloud SQL")
