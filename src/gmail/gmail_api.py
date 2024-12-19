# src/gmail/gmail_api.py

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import html

# Load environment variables
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Authenticate and set up Gmail API
def authenticate_gmail():
    """
    Authenticate and set up the Gmail API client.

    Checks for existing credentials in `token.json`. If credentials
    are invalid or do not exist, initiates the OAuth2 flow to generate new credentials.

    Returns:
        google.oauth2.credentials.Credentials: Authenticated credentials for the API.

    Raises:
        FileNotFoundError: If `credentials.json` is not found in the current directory.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Fetch unread emails from Gmail
def fetch_unread_emails(service, num_emails: int = 5) -> list:
    """
    Fetch unread emails from the user's Gmail inbox.

    Args:
        service: The Gmail API service instance.
        num_emails (int, optional): The maximum number of unread emails to fetch. Defaults to 5.

    Returns:
        list: A list of dictionaries containing email subjects and snippets. 
              Each dictionary has the structure:
              {
                  "subject": <email_subject>,
                  "snippet": <email_snippet>
              }

    Raises:
        googleapiclient.errors.HttpError: If the API request fails.
    """
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])
    email_texts = []
    if not messages:
        return email_texts

    # Limit the number of emails to fetch based on num_emails parameter
    for msg in messages[:num_emails]:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        subject = ''
        for header in message['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        # Decode HTML entities in the snippet
        snippet = html.unescape(message.get('snippet', ''))

        # Append email details as a dictionary
        email_texts.append({
            "subject": subject,
            "snippet": snippet
        })

    return email_texts