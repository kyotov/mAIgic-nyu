from flask import Flask, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Load credentials from environment variables (replace with actual environment variables in production)
CLIENT_ID = '7855184757495.7892528086800'
CLIENT_SECRET = '918fec90decd47b23d25fe58e02a73e1'

@app.route('/')
def home():
    return "Welcome to the Slack OAuth Handler! Ready to authenticate."

@app.route('/oauth/callback', methods=['GET', 'POST'])
def oauth_callback():
    # Retrieve the authorization code from the query string
    code = request.args.get('code')
    if not code:
        return 'Error: Missing authorization code.', 400

    # Prepare the data for exchanging the code for a token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'https://two-animals-double.loca.lt/oauth/callback'  # Ensure this matches your LocalTunnel URL
    }

    # Make a POST request to Slack's OAuth API
    try:
        response = requests.post('https://slack.com/api/oauth.v2.access', data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to Slack's OAuth API: {e}", 500
    
    # Process the response
    response_json = response.json()
    if response_json.get('ok'):
        # Access token received
        token = response_json.get('access_token')
        # Log or store the token securely (e.g., in a database)
        return redirect(url_for('success'))
    else:
        # Handle any errors from Slack
        error_message = response_json.get('error', 'Unknown error')
        return f"Failed to retrieve access token: {error_message}", 400

@app.route('/success')
def success():
    return "OAuth flow completed successfully!"

if __name__ == '__main__':
    app.run(port=3000, debug=True)
