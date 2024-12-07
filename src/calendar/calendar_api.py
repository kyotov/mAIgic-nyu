# src/calendar/calendar_api.py

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Load environment variables
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate and set up Google Calendar API
def authenticate_google_calendar():
    """
    Authenticate and set up the Google Calendar API client.

    Checks for existing credentials in `token_calendar.json`. If credentials
    are invalid or do not exist, initiates the OAuth2 flow to generate new credentials.

    Returns:
        google.oauth2.credentials.Credentials: Authenticated credentials for the API.

    Raises:
        FileNotFoundError: If `credentials.json` is not found in the current directory.
    """
    creds = None
    if os.path.exists('token_calendar.json'):
        creds = Credentials.from_authorized_user_file('token_calendar.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_calendar.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Add an event to Google Calendar
def add_event_to_calendar(task_name: str, due_date: str) -> str:
    """
    Add a new event to the user's primary Google Calendar.

    Args:
        task_name (str): The name or summary of the event.
        due_date (str): The start and end time of the event in ISO 8601 format 
                        (e.g., '2024-12-04T10:00:00-07:00').

    Returns:
        str: The unique event ID of the created event.

    Raises:
        googleapiclient.errors.HttpError: If the event creation fails.
    """
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    event = {
        'summary': task_name,
        'start': {
            'dateTime': due_date,
        },
        'end': {
            'dateTime': due_date,
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event['id']

# Update an existing event in Google Calendar
def update_calendar_event(event_id: str, task_name: str, due_date: str) -> dict:
    """
    Update an existing event in the user's primary Google Calendar.

    Args:
        event_id (str): The unique ID of the event to be updated.
        task_name (str): The updated name or summary of the event.
        due_date (str): The updated start and end time of the event in ISO 8601 format.

    Returns:
        dict: The updated event resource.

    Raises:
        googleapiclient.errors.HttpError: If the event update fails.
    """
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = task_name
    event['start']['dateTime'] = due_date
    event['end']['dateTime'] = due_date
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event

# Delete an event from Google Calendar
def delete_calendar_event(event_id : str) -> None:
    """
    Delete an event from the user's primary Google Calendar.

    Args:
        event_id (str): The unique ID of the event to be deleted.

    Returns:
        None

    Raises:
        googleapiclient.errors.HttpError: If the event deletion fails.
    """
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    service.events().delete(calendarId='primary', eventId=event_id).execute()