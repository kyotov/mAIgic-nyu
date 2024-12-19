# tests/test_trello/test_trello_bot.py

import pytest
from unittest.mock import patch, MagicMock
from src.trello.trello_bot import TrelloBot, card_event_map

@pytest.fixture
def trello_bot():
    return TrelloBot()

@patch('src.trello.trello_bot.TrelloClient')
def test_add_card_and_map_event(mock_trello_client_class):
    # Create a mock TrelloClient instance
    mock_trello_client = MagicMock()
    mock_trello_client.add_card_to_trello.return_value = {'id': 'card_id_999'}

    # When TrelloBot is instantiated, it creates a TrelloClient. Return the mock instead.
    mock_trello_client_class.return_value = mock_trello_client

    bot = TrelloBot()
    event_id = 'event_12345'
    card_id = bot.add_card_and_map_event('Test Card', 'TestList', event_id)

    assert card_id == 'card_id_999'
    assert card_event_map[card_id] == event_id
    mock_trello_client.add_card_to_trello.assert_called_once_with('Test Card', 'TestList')