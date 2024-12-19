# tests/test_slack/test_slack_bot.py

import pytest
from unittest.mock import patch, MagicMock
from slack_sdk.web.client import WebClient

from src.slack.slack_bot import (
    add_to_trello_task,
    remove_from_trello_task,
    delete_trello_list,
    show_tasks_in_list,
    handle_fetch_emails,
    handle_show_emails,
)

# Helper function to simulate messages
def create_message_event(text):
    return {'channel': 'C12345', 'user': 'U12345', 'text': text}

def create_context(matches):
    return {'matches': matches}

# Mock the 'say' function
@pytest.fixture
def say():
    return MagicMock()


@patch('src.slack.slack_bot.trello_client.add_card_to_trello')
@patch('src.slack.slack_bot.post_to_slack')
def test_add_to_trello_task(mock_post_to_slack, mock_add_card, say):
    mock_add_card.return_value = {'id': 'card_id_12345'}
    message = create_message_event('add "Test Task" to TestList by 2023-12-31 23:59')
    context = create_context(['Test Task', 'TestList', '2023-12-31 23:59'])
    add_to_trello_task(message=message, say=say, context=context)
    mock_add_card.assert_called_once()
    mock_post_to_slack.assert_called_once()


@patch('src.slack.slack_bot.trello_client.delete_card_from_trello')
@patch('src.slack.slack_bot.post_to_slack')
def test_remove_from_trello_task(mock_post_to_slack, mock_delete_card, say):
    mock_delete_card.return_value = 'card_id_12345'
    message = create_message_event('remove "Test Task" from TestList')
    context = create_context(['Test Task', 'TestList'])
    remove_from_trello_task(message=message, say=say, context=context)
    mock_delete_card.assert_called_once()
    mock_post_to_slack.assert_called_once()


@patch('src.slack.slack_bot.trello_client.archive_trello_list')
@patch('src.slack.slack_bot.post_to_slack')
def test_delete_trello_list(mock_post_to_slack, mock_archive_list, say):
    mock_archive_list.return_value = True
    message = create_message_event('delete list TestList')
    context = create_context(['TestList'])
    delete_trello_list(message=message, say=say, context=context)
    mock_archive_list.assert_called_once()
    mock_post_to_slack.assert_called_once()


@patch('src.slack.slack_bot.trello_client.get_trello_cards')
@patch('src.slack.slack_bot.post_to_slack')
def test_show_tasks_in_list(mock_post_to_slack, mock_get_cards, say):
    mock_get_cards.return_value = [{'name': 'Task 1'}, {'name': 'Task 2'}]
    message = create_message_event('show me tasks in TestList')
    context = create_context(['TestList'])
    show_tasks_in_list(message=message, say=say, context=context)
    mock_get_cards.assert_called_once()
    mock_post_to_slack.assert_called_once()


@patch('src.slack.slack_bot.fetch_and_post_emails')
def test_handle_fetch_emails(mock_fetch_emails, say):
    message = create_message_event('fetch emails')
    handle_fetch_emails(message=message, say=say)
    mock_fetch_emails.assert_called_once()


@patch('src.slack.slack_bot.fetch_and_post_emails')
def test_handle_show_emails(mock_fetch_emails, say):
    message = create_message_event('show me 3 emails')
    context = create_context(['3'])
    handle_show_emails(message=message, say=say, context=context)
    mock_fetch_emails.assert_called_once_with(3)