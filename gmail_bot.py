import os
import time
from slack_sdk import WebClient
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import html

# Load environment variables
load_dotenv()

# Environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")  # Add this to your .env file
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Set up Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Authenticate and set up Gmail API
def authenticate_gmail():
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
def fetch_unread_emails(service, num_emails=5):
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


# Send fetched emails to Slack
def post_emails_to_slack():
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    emails = fetch_unread_emails(service)
    if not emails:
        slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text="No new unread emails.")
        return

    for email in emails:
        message = {
            "text": "*New Email Received*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Subject*: {email['subject']}\n*Snippet*: {email['snippet']}"
                    }
                }
            ]
        }
        slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, **message)


# Fetch and post a specific number of emails to Slack on demand
def fetch_and_post_emails(num_emails=5):
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    emails = fetch_unread_emails(service, num_emails=num_emails)
    if not emails:
        slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text="No new unread emails.")
        return

    for email in emails:
        message = {
            "text": "*New Email Received*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Subject*: {email['subject']}\n*Snippet*: {email['snippet']}"
                    }
                }
            ]
        }
        slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, **message)



# Run this function periodically
def run_gmail_to_slack():
    while True:
        post_emails_to_slack()
        time.sleep(300)  # Check for new emails every 5 minutes
