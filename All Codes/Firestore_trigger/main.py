import functions_framework
import json

@functions_framework.cloud_event
def on_user_create(cloud_event):
    """
    Cloud Functions Gen 2
    Firestore CREATE Trigger
    Database: bhanu-db
    Collection: users
    """

    data = cloud_event.data or {}
    value = data.get("value", {})
    fields = value.get("fields", {})

    def get_string(field):
        return fields.get(field, {}).get("stringValue")

    def get_int(field):
        val = fields.get(field, {}).get("integerValue")
        return int(val) if val is not None else None

    name = get_string("name")
    email = get_string("email")
    course = get_string("course")
    profession = get_string("profession")  
    exp = get_int("exp")

    print("FIRESTORE CREATE EVENT RECEIVED")
    print(json.dumps({
        "document": value.get("name"),
        "name": name,
        "email": email,
        "course": course,
        "profession": profession,
        "exp": exp
    }, indent=2))

    if exp is not None and exp < 0:
        print(" Invalid experience value detected")

    print(" Function execution completed successfully")
