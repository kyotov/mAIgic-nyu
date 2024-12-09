from googleapiclient.discovery import build
from src.gmail.auth import get_credentials
from src.gmail.models import Email, Header

class GmailAPI:
    """class to actually interact with the mails"""
    def __init__(self):
        self.service = build('gmail', 'v1', credentials=get_credentials())

    def fetch_latest_email(self):
        results = self.service.users().messages().list(userId='me', maxResults=1).execute()
        messages = results.get('messages', [])
        if messages:
            email_data = self.service.users().messages().get(userId='me', id=messages[0]['id']).execute()
            headers = email_data.get('payload', {}).get('headers', [])
            sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            snippet = email_data.get('snippet', 'No Snippet Available')
            header_objects = [Header(header['name'], header['value']) for header in headers]
            return Email(email_id=email_data['id'], sender=sender, subject=subject, snippet=snippet, headers=header_objects)
        return None
