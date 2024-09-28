import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage

# If modifying these SCOPES, delete the token.json file and authorize again.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/chat.bot']

# Authenticate and build the Gmail API service
def gmail_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if False and creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open('token.json', 'w') as token:
        #     token.write(creds.to_json())

    return (build('gmail', 'v1', credentials=creds), build('chat', 'v1', credentials=creds))

# List the latest emails in the inbox
def list_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages.')
    else:
        print('Message snippets:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            snippet = msg['snippet']
            print(f"- {snippet}")

def send_chat_message(chat):
    # Replace 'spaces/XXXXX' with your space ID
    space = 'spaces/AAAAfsxkCyA'
    # https://chat.google.com/room/AAAAfsxkCyA?cls=7

    message = {
        'text': 'Hello from Python via Google Chat API!'
    }

    # Send the message
    result = chat.spaces().messages().create(
        parent=space,
        body=message
    ).execute()
    
if __name__ == '__main__':
    gmail, gchat = gmail_authenticate()
    # list_emails(gmail)
    send_chat_message(gchat)
