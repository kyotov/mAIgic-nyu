from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token='xoxb-7855184757495-7855216149575-kPNmwbhC4mlAyVyUT7QXWpkJ')

def send_message(channel, message):
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print("Message sent successfully:", response["message"]["text"])
    except SlackApiError as e:
        print("Error sending message:", e.response["error"])

app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    elif 'event' in data:
        event = data['event']
        if event['type'] == 'message' and 'subtype' not in event:
            # Check the message text and respond appropriately
            user_message = event['text'].lower()
            if "hello" in user_message:
                send_message(event['channel'], "Hello there! How can I help you?")
            elif "help" in user_message:
                send_message(event['channel'], "Here's a list of commands you can use...")
            else:
                send_message(event['channel'], "I'm not sure how to respond to that.")
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
