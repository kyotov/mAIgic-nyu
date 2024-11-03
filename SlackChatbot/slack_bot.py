from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from trello import TrelloClient
import threading
import time
import os
import re

# Initialize Slack and Trello clients
client = WebClient(token='xoxb-7855184757495-7855216149575-KI6lOoBXKSoudrc9pzugoW0x')
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
trello_client = TrelloClient(api_key=TRELLO_API_KEY, api_secret=TRELLO_TOKEN)

app = Flask(__name__)
processed_event_ids = set()

def clear_processed_ids():
    """Periodically clear old event IDs to prevent memory issues."""
    while True:
        time.sleep(300)  # Clear every 5 minutes
        processed_event_ids.clear()

threading.Thread(target=clear_processed_ids, daemon=True).start()

def send_message(channel, message):
    """Send a message to a Slack channel."""
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print("Message sent successfully:", response["message"]["text"])
    except SlackApiError as e:
        print("Error sending message:", e.response["error"])

def create_trello_card(board_name, list_name, card_name, card_desc=""):
    """Create a Trello card in a specified board and list."""
    try:
        board = next((b for b in trello_client.list_boards() if b.name == board_name), None)
        if not board:
            return f"Board '{board_name}' not found."

        todo_list = next((lst for lst in board.list_lists() if lst.name == list_name), None)
        if not todo_list:
            return f"List '{list_name}' not found on board '{board_name}'."

        todo_list.add_card(name=card_name, desc=card_desc)
        return f"Card '{card_name}' created in '{list_name}' list on board '{board_name}'."
    except Exception as e:
        return f"Error creating Trello card: {str(e)}"

def process_event(event):
    """Process the Slack event if it's not from the bot itself."""
    if 'bot_id' in event:
        return  # Ignore events from the bot itself

    user_message = event['text'].lower()

    # Handle basic commands
    if "hello" in user_message:
        send_message(event['channel'], "Hello there! How can I help you?")
    elif "help" in user_message:
        send_message(event['channel'], "Here's a list of commands you can use...")
    
    # Trello task command: Detect if user asks to add a task to Trello
    elif match := re.match(r'add "(.*?)" to trello', user_message, re.IGNORECASE):
        task_name = match.group(1)
        # Define board and list names as per your Trello setup
        board_name = "Your Board Name"  # Replace with your Trello board name
        list_name = "To Do"  # Replace with the list name you want to use

        # Create Trello card and send a response
        response_message = create_trello_card(board_name, list_name, task_name)
        send_message(event['channel'], response_message)
    
    else:
        send_message(event['channel'], "I'm not sure how to respond to that.")

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400

    # Respond to Slack's URL verification challenge
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})

    # Process actual events
    elif 'event' in data:
        event = data['event']
        event_id = data.get('event_id')

        # Deduplicate based on event_id
        if event_id in processed_event_ids:
            print(f"Duplicate event ignored: {event_id}")
            return '', 200

        processed_event_ids.add(event_id)
        print(f"Event received and processing started: {event_id}")

        # Process the event in a separate thread
        threading.Thread(target=process_event, args=(event,)).start()

    return '', 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)
