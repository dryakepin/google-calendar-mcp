# Google Calendar API with Flask

This project provides a Flask-based API to interact with the Google Calendar API. It allows you to create, list, update, and delete calendar events.

## Features

- Create a new calendar event.
- List events within a specified time range.
- Update an existing event.
- Delete an event.

## Setup

### 1. Prerequisites

- Python 3.6+
- A Google Cloud Platform project with the Google Calendar API enabled.
- OAuth 2.0 Client IDs credentials from the Google Cloud Console.

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dryakepin/google-calendar-mcp.git
    cd google-calendar-mcp
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

Set the following environment variables. You can create a `.env` file and use a library like `python-dotenv` to manage them.

- `GOOGLE_CLIENT_ID`: Your Google Cloud project's client ID.
- `GOOGLE_CLIENT_SECRET`: Your Google Cloud project's client secret.
- `API_SECRET_KEY`: A secret key of your choice to use as a bearer token for authenticating API requests.

**Example `.env` file:**
```
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
API_SECRET_KEY="your-super-secret-key"
```

## Running the Application

1.  **Start the Flask server:**
    ```bash
    python main.py
    ```
    The application will be running on `http://127.0.0.1:5000`.

## API Usage

All requests must include an `Authorization` header with a bearer token.

**Example Header:**
`Authorization: Bearer your-super-secret-key`

### Create Event

- **URL:** `/create_event`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "user_id": "some_user_id",
    "title": "My Awesome Event",
    "start_time": "2024-12-01T10:00:00Z",
    "end_time": "2024-12-01T12:00:00Z",
    "attendees": ["friend1@example.com", "friend2@example.com"],
    "location": "My Place"
  }
  ```

### List Events

- **URL:** `/list_events`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "user_id": "some_user_id",
    "start_time": "2024-12-01T00:00:00Z",
    "end_time": "2024-12-31T23:59:59Z"
  }
  ```

### Update Event

- **URL:** `/update_event`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "user_id": "some_user_id",
    "event_id": "the-event-id-to-update",
    "title": "My Updated Awesome Event"
  }
  ```

### Delete Event

- **URL:** `/delete_event`
- **Method:** `POST`
- **Body (JSON):**
  ```json
  {
    "user_id": "some_user_id",
    "event_id": "the-event-id-to-delete"
  }
  ``` 