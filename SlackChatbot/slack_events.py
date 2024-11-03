from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from trello import TrelloClient
import re
import os

app = Flask(__name__)

# Slack and Trello client setup
client = WebClient(token='xoxb-your-slack-token')
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
trello_client = TrelloClient(api_key=TRELLO_API_KEY, api_secret=TRELLO_TOKEN)

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

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    # Slack URL verification challenge
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    
    # Process Slack events
    elif 'event' in data:
        event = data['event']
        
        # Only handle messages without subtypes (direct messages)
        if event['type'] == 'message' and 'subtype' not in event:
            user_message = event['text'].lower()
            channel = event['channel']

            # Detect Trello task creation command
            match = re.match(r'add "(.*?)" to trello', user_message, re.IGNORECASE)
            if match:
                task_name = match.group(1)
                
                # Specify your board and list names
                board_name = "Your Board Name"  # Replace with your Trello board name
                list_name = "To Do"  # Replace with the Trello list name

                # Call Trello card creation function
                response_message = create_trello_card(board_name, list_name, task_name)
                
                # Send response back to Slack
                send_message(channel, response_message)
            else:
                send_message(channel, "I'm not sure how to respond to that.")
                
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
