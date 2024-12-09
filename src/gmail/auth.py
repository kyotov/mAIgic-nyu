import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

def get_credentials():
    """gmail api authentication of credentials"""
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    token_path = 'token.json'
    creds_path = os.getenv('GOOGLE_CREDENTIALS_JSON')

    if not creds_path:
        raise FileNotFoundError("Environment variable 'GOOGLE_CREDENTIALS_JSON' is not set or missing.")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
    return creds
