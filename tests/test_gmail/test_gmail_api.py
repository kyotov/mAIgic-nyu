# tests/test_gmail/test_gmail_api.py

import pytest
from unittest.mock import patch, MagicMock
from src.gmail.gmail_api import authenticate_gmail, fetch_unread_emails

@patch('src.gmail.gmail_api.build')
def test_fetch_unread_emails_no_emails(mock_build):
    # Mock the service
    mock_service = MagicMock()
    mock_users = mock_service.users.return_value
    mock_messages = mock_users.messages.return_value
    mock_list = mock_messages.list.return_value
    mock_list.execute.return_value = {'messages': []}
    mock_build.return_value = mock_service

    emails = fetch_unread_emails(mock_service)
    assert emails == []

@patch('src.gmail.gmail_api.build')
def test_fetch_unread_emails_with_emails(mock_build):
    mock_service = MagicMock()
    mock_users = mock_service.users.return_value
    mock_messages = mock_users.messages.return_value

    # Mock list
    mock_list = mock_messages.list.return_value
    mock_list.execute.return_value = {
        'messages': [{'id': 'message_id_1'}, {'id': 'message_id_2'}]
    }

    # Mock get
    def mock_get(userId, id):
        get_result = MagicMock()
        get_result.execute.return_value = {
            'id': id,
            'snippet': 'Email snippet',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': f'Subject {id}'}
                ]
            }
        }
        return get_result

    mock_messages.get.side_effect = mock_get
    mock_build.return_value = mock_service

    emails = fetch_unread_emails(mock_service, num_emails=2)
    assert len(emails) == 2
    assert emails[0]['subject'] == 'Subject message_id_1'
    assert emails[1]['subject'] == 'Subject message_id_2'