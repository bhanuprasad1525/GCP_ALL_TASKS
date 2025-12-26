import base64
import json
import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        unix_socket=os.environ["DB_SOCKET"]  
    )


def pubsub_to_cloudsql(cloud_event):
  
    try:
       
        message = cloud_event.data["message"]
        data = base64.b64decode(message["data"]).decode("utf-8")
        payload = json.loads(data)

        user = payload.get("user")
        event = payload.get("event")

        print("Message received:", payload)


        conn = get_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO user_events (user_name, event_name)
            VALUES (%s, %s)
        """

        cursor.execute(insert_query, (user, event))
        conn.commit()

        cursor.close()
        conn.close()

        print("Data inserted into Cloud SQL")

    except Exception as e:
        print("Error processing message:", str(e))
