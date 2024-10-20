from flask import Flask, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Load credentials from environment variables
CLIENT_ID = '7855184757495.7892528086800'
CLIENT_SECRET = '918fec90decd47b23d25fe58e02a73e1'

@app.route('/')
def home():
    return "Welcome to the Slack OAuth Handler! Ready to authenticate."

@app.route('/oauth/callback')
def oauth_callback():
    # Retrieve the code from the query string
    code = request.args.get('code')
    if not code:
        return 'Error: Missing authorization code.', 400

    # Prepare the request data for exchanging the code for a token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    }

    # Make a POST request to Slack's OAuth API to exchange the code for an access token
    response = requests.post('https://slack.com/api/oauth.v2.access', data=data)
    
    # Check if the request was successful
    response_json = response.json()
    if response.status_code == 200 and response_json.get('ok'):
        # Extract the token from the response
        token = response_json.get('access_token')
        # Log or store the token securely (e.g., in a database)
        return redirect(url_for('success'))
    else:
        error_message = response_json.get('error', 'Unknown error')
        return f"Failed to retrieve access token: {error_message}", 400

@app.route('/success')
def success():
    return "OAuth flow completed successfully!"

if __name__ == '__main__':
    app.run(port=3000, debug=True)
