# app.py

import threading
from src.slack.slack_bot import run_slack_bot
from src.gmail.gmail_bot import run_gmail_to_slack

if __name__ == "__main__":
    # Start Gmail bot in a separate thread
    gmail_thread = threading.Thread(target=run_gmail_to_slack)
    gmail_thread.start()

    # Start Slack bot
    run_slack_bot()