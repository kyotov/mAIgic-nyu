# tests/test_gmail/test_gmail_bot.py

import pytest
from unittest.mock import patch, MagicMock
from src.gmail.gmail_bot import (
    post_emails_to_slack,
    fetch_and_post_emails,
)
import os

@patch('src.gmail.gmail_bot.authenticate_gmail')
@patch('src.gmail.gmail_bot.build')
@patch('src.gmail.gmail_bot.fetch_unread_emails')
@patch('src.gmail.gmail_bot.slack_client')
def test_fetch_and_post_emails(mock_slack_client, mock_fetch_emails, mock_build, mock_authenticate_gmail):
    # Set up the mocks
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    mock_authenticate_gmail.return_value = MagicMock()
    mock_fetch_emails.return_value = [
        {'subject': 'Test Subject', 'snippet': 'Test Snippet'}
    ]
    mock_slack_client.chat_postMessage.return_value = None

    # Call the function under test
    fetch_and_post_emails(num_emails=1)

    # Assertions
    mock_fetch_emails.assert_called_once_with(
        mock_service,
        num_emails=1
    )
    mock_slack_client.chat_postMessage.assert_called_once()