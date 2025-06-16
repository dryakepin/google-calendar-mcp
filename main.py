
from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "https://yourdomain.com/oauth2callback"

# Simulated secure token retrieval (replace with DB lookup in production)
def get_user_token(user_id):
    return {
        "access_token": "ya29.a0AfH6SM...",
        "refresh_token": "1//0g..."
    }

def get_calendar_service(user_id):
    token = get_user_token(user_id)
    creds = Credentials(token=token["access_token"],
                        refresh_token=token["refresh_token"],
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET)
    return build("calendar", "v3", credentials=creds)

@app.route("/create_event", methods=["POST"])
def create_event():
    data = request.json
    service = get_calendar_service(data["user_id"])
    event = {
        "summary": data["title"],
        "location": data.get("location", ""),
        "start": {
            "dateTime": data["start_time"],
            "timeZone": "Europe/Copenhagen",
        },
        "end": {
            "dateTime": data["end_time"],
            "timeZone": "Europe/Copenhagen",
        },
        "attendees": [{"email": email} for email in data.get("attendees", [])],
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return jsonify({"eventId": created_event["id"]})

@app.route("/list_events", methods=["POST"])
def list_events():
    data = request.json
    service = get_calendar_service(data["user_id"])
    events_result = service.events().list(
        calendarId="primary",
        timeMin=data["start_time"],
        timeMax=data["end_time"],
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = [{
        "id": e["id"],
        "title": e.get("summary", ""),
        "start_time": e["start"].get("dateTime", ""),
        "end_time": e["end"].get("dateTime", ""),
        "attendees": [a["email"] for a in e.get("attendees", [])],
        "location": e.get("location", "")
    } for e in events_result.get("items", [])]
    return jsonify({"events": events})

@app.route("/update_event", methods=["POST"])
def update_event():
    data = request.json
    service = get_calendar_service(data["user_id"])
    event = service.events().get(calendarId="primary", eventId=data["event_id"]).execute()

    if "title" in data:
        event["summary"] = data["title"]
    if "start_time" in data:
        event["start"]["dateTime"] = data["start_time"]
        event["start"]["timeZone"] = "Europe/Copenhagen"
    if "end_time" in data:
        event["end"]["dateTime"] = data["end_time"]
        event["end"]["timeZone"] = "Europe/Copenhagen"
    if "attendees" in data:
        event["attendees"] = [{"email": email} for email in data["attendees"]]
    if "location" in data:
        event["location"] = data["location"]

    updated_event = service.events().update(calendarId="primary", eventId=data["event_id"], body=event).execute()
    return jsonify({"status": "success", "eventId": updated_event["id"]})

@app.route("/delete_event", methods=["POST"])
def delete_event():
    data = request.json
    service = get_calendar_service(data["user_id"])
    service.events().delete(calendarId="primary", eventId=data["event_id"]).execute()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
