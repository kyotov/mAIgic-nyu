# src/gmail/gmail_bot.py

import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from .gmail_api import authenticate_gmail, fetch_unread_emails
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables
load_dotenv()

# Environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# Set up Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Send fetched emails to Slack
def post_emails_to_slack() -> None:
    """
    Fetch unread emails from Gmail and post them to a Slack channel.

    If no unread emails are found, a message is posted indicating no new emails.

    Returns:
        None

    Raises:
        googleapiclient.errors.HttpError: If Gmail API requests fail.
        slack_sdk.errors.SlackApiError: If Slack API requests fail.
    """
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    emails = fetch_unread_emails(service)
    if not emails:
        try:
            slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text="No new unread emails.")
        except SlackApiError as e:
            print(f"Error posting to Slack: {e.response['error']}")
        return

    for email in emails:
        message = {
            "text": "*New Email Received*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Subject*: {email['subject']}\n*Snippet*: {email['snippet']}"
                    }
                }
            ]
        }
        try:
            slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, **message)
        except SlackApiError as e:
            print(f"Error posting to Slack: {e.response['error']}")

# Fetch and post a specific number of emails to Slack on demand
def fetch_and_post_emails(num_emails: int = 5) -> None:
    """
    Fetch a specific number of unread emails from Gmail and post them to a Slack channel.

    Args:
        num_emails (int, optional): The number of unread emails to fetch. Defaults to 5.

    Returns:
        None

    Raises:
        googleapiclient.errors.HttpError: If Gmail API requests fail.
        slack_sdk.errors.SlackApiError: If Slack API requests fail.
    """
    service = build('gmail', 'v1', credentials=authenticate_gmail())
    emails = fetch_unread_emails(service, num_emails=num_emails)
    if not emails:
        try:
            slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text="No new unread emails.")
        except SlackApiError as e:
            print(f"Error posting to Slack: {e.response['error']}")
        return

    for email in emails:
        message = {
            "text": "*New Email Received*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Subject*: {email['subject']}\n*Snippet*: {email['snippet']}"
                    }
                }
            ]
        }
        try:
            slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, **message)
        except SlackApiError as e:
            print(f"Error posting to Slack: {e.response['error']}")

# Run this function periodically
def run_gmail_to_slack() -> None:
    """
    Periodically fetch unread emails from Gmail and post them to Slack.

    This function runs indefinitely, checking for new emails every 5 minutes.

    Returns:
        None
    """
    while True:
        post_emails_to_slack()
        time.sleep(3000)  # Check for new emails every 5 minutes