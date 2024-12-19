# src/slack/slack_api.py

import os
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Initialize the Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Function to post a message to a Slack channel
def post_to_slack(channel: str, message: str) -> dict:
    """
    Post a message to a specific Slack channel.

    Args:
        channel (str): The Slack channel ID or name where the message will be posted.
        message (str): The message text to post.

    Returns:
        dict: The response from Slack API containing details about the posted message.

    Raises:
        slack_sdk.errors.SlackApiError: If the Slack API request fails.
    """
    response = slack_client.chat_postMessage(channel=channel, text=message)
    return response