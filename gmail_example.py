import os.path
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


from src.gmail.models import GMailMessage

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# , 'https://www.googleapis.com/auth/chat.bot']


def gmail_authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return (
        build("gmail", "v1", credentials=creds),
        build("chat", "v1", credentials=creds),
    )


def list_emails(service):
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=10)
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No new messages.")
    else:
        print("Message snippets:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            pprint(message["id"])
            m = GMailMessage(msg)
            with open(f"email_examples/{message['id']}.email", "w") as f:
                f.write(m.as_md())


# def send_chat_message(chat):
#     space = "spaces/AAAAfsxkCyA"
#     message = {"text": "Hello from Python via Google Chat API!"}
#     chat.spaces().messages().create(parent=space, body=message).execute()


if __name__ == "__main__":
    gmail, gchat = gmail_authenticate()
    list_emails(gmail)
    # send_chat_message(gchat)
