from googleapiclient.discovery import build
from google.oauth2 import service_account

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'maigic-assistant-key.json'

# Scopes required for the Google Chat API
SCOPES = ['https://www.googleapis.com/auth/chat.bot']

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def send_message(space_id, text):
    """Sends a message to a Google Chat space using the Chat API."""
    chat = build('chat', 'v1', credentials=credentials)
    
    response = chat.spaces().list().execute()
    for space in response.get('spaces', []):
        print(f"Space name: {space['name']}, Display name: {space.get('displayName', 'No name')}")
    
    message = {'text': text}

    response = chat.spaces().messages().create(
        parent=f'spaces/{space_id}',
        body=message
    ).execute()
    
    print(f'Message sent: {response}')

# Example usage
if __name__ == '__main__':
    # Replace with your space ID
    space_id = 'AAAAfsxkCyA'
    send_message(space_id, 'Hello from my app via Google Chat API!')
