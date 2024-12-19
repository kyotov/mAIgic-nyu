# tests/test_slack/test_slack_api.py

import pytest
from unittest.mock import patch
from src.slack.slack_api import post_to_slack

@patch('src.slack.slack_api.slack_client')
def test_post_to_slack(mock_slack_client):
    channel = '#test-channel'
    message = 'Test Message'

    post_to_slack(channel, message)

    mock_slack_client.chat_postMessage.assert_called_once_with(channel=channel, text=message)