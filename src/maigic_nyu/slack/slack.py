import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.error import BoltError


# Load environment variables
load_dotenv()

# Attempts to initializes app with bot token and socket mode handler
try:
    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
    # Response if any message is sent in any channel
    @app.message()
    def handle_message(message, say):
        # Define external function handler, depending on desired implementation
        
        # Placeholder: say() sends a message to the channel where the event was triggered
        say(f"Hey there <@{message['user']}>! I am responding to: {message['text']}")

except BoltError as e:
    # Generally, this error arises if the "SLACK_BOT_TOKEN" is invalid
    print("Error initializing Slack App:", e)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()