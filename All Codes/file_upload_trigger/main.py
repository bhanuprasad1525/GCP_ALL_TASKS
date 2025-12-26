from datetime import datetime
import functions_framework

@functions_framework.cloud_event
def on_file_upload(cloud_event):
    data = cloud_event.data

    file_name = data.get("name")
    bucket_name = data.get("bucket")
    content_type = data.get("contentType")
    size = data.get("size")
    time_created = data.get("timeCreated")

    print(" New file uploaded")
    print("Bucket:", bucket_name)
    print("File:", file_name)
    print("Type:", content_type)
    print("Size:", size)
    print("Uploaded at:", time_created or datetime.utcnow())
