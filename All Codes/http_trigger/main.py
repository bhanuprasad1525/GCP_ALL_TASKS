import json
from datetime import datetime


def http_trigger(request):
  

    if request.method == "GET":
        return {
            "message": "HTTP GET request received",
            "timestamp": datetime.utcnow().isoformat()
        }, 200

    if request.method == "POST":
        request_json = request.get_json(silent=True)

        if not request_json:
            return {"error": "Invalid or missing JSON"}, 400

        user = request_json.get("user")
        action = request_json.get("action")

        response = {
            "status": "success",
            "user": user,
            "action": action,
            "processed_at": datetime.utcnow().isoformat()
        }

        return response, 200

    return {"error": "Method not allowed"}, 405
