import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate and set up Google Calendar API
def authenticate_google_calendar():
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
def add_event_to_calendar(task_name, due_date):
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    event = {
        'summary': task_name,
        'start': {
            'dateTime': due_date,  # due_date already includes timezone info
        },
        'end': {
            'dateTime': due_date,  # Set the end time the same as start for simplicity
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event['id']


# Update an existing event in Google Calendar
def update_calendar_event(event_id, task_name, due_date):
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    event['summary'] = task_name
    event['start']['dateTime'] = due_date
    event['end']['dateTime'] = due_date
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event

# Delete an event from Google Calendar
def delete_calendar_event(event_id):
    service = build('calendar', 'v3', credentials=authenticate_google_calendar())
    service.events().delete(calendarId='primary', eventId=event_id).execute()
