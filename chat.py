from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import chat_v1 as google_chat
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/chat.spaces.readonly', 'https://www.googleapis.com/auth/chat.bot']


def main():
    """Shows basic usage of the Google Chat API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Create a client
        client = google_chat.ChatServiceClient(
            credentials = creds,
            client_options = {
                "scopes" : SCOPES
            }
        )

        # Initialize request argument(s)
        request = google_chat.ListSpacesRequest(
            # Filter spaces by space type (SPACE or GROUP_CHAT or DIRECT_MESSAGE)
            filter = 'space_type = "SPACE"'
        )

        # Make the request
        page_result = client.list_spaces(request)

        # Handle the response. Iterating over page_result will yield results and
        # resolve additional pages automatically.
        for response in page_result:
            print(response)

        send_message("AAAAfsxkCyA", "heya!")
    except Exception as error:
        # TODO(developer) - Handle errors from Chat API.
        print(f'An error occurred: {error}')

def send_message(space_id, text):
    """Sends a message to a Google Chat space using the Chat API."""
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    chat = build('chat', 'v1', credentials=creds)
    message = {'text': text}

    response = chat.spaces().messages().create(
        parent=f'spaces/{space_id}',
        body=message
    ).execute()
    
    print(f'Message sent: {response}')

# Example usage
if __name__ == '__main__':
    main()
