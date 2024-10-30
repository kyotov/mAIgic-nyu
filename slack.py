import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


# Load environment variables
load_dotenv()

# Initializes app with bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Response if any message is sent in any channel
@app.message()
def message_hello(message, say):
        
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>! I am responding to: {message['text']}")

# Starts app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    