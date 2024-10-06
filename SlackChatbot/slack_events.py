from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    # Slack sends a challenge parameter when verifying the request URL
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    # Your logic for other events
    elif 'event' in data:
        event = data['event']
        if event['type'] == 'message' and 'subtype' not in event:
            # Logic to handle incoming messages
            # Respond to messages or other interactions here
            pass
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
