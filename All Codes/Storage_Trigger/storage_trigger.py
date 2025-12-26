import functions_framework

@functions_framework.cloud_event
def storage_trigger(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    file_name = data["name"]
    size = data.get("size", "Unknown")

    print(f" File uploaded!")
    print(f"Bucket: {bucket}")
    print(f"File: {file_name}")
    print(f"Size: {size} bytes")
