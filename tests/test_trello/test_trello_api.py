# tests/test_trello/test_trello_api.py

import pytest
from unittest.mock import patch, MagicMock
from src.trello.trello_api import TrelloClient, TRELLO_API_BASE

@pytest.fixture
def trello_client():
    return TrelloClient(api_key='test_key', token='test_token', board_id='test_board_id')

@patch('src.trello.trello_api.requests.get')
def test_get_trello_list_id_existing(mock_get, trello_client):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'id': 'list_id_12345', 'name': 'TestList'}]
    list_id = trello_client.get_trello_list_id('TestList')
    assert list_id == 'list_id_12345'
    mock_get.assert_called_once_with(
        f"{TRELLO_API_BASE}/boards/test_board_id/lists",
        params={'key': 'test_key', 'token': 'test_token', 'filter': 'open'}
    )

@patch('src.trello.trello_api.requests.get')
def test_get_trello_list_id_non_existing(mock_get, trello_client):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = []
    list_id = trello_client.get_trello_list_id('NonExistingList')
    assert list_id is None
    mock_get.assert_called_once()

@patch('src.trello.trello_api.requests.post')
def test_create_trello_list(mock_post, trello_client):
    mock_post.return_value = MagicMock(status_code=200)
    mock_post.return_value.json.return_value = {'id': 'new_list_id_67890'}
    list_id = trello_client.create_trello_list('NewList')
    assert list_id == 'new_list_id_67890'
    mock_post.assert_called_once_with(
        f"{TRELLO_API_BASE}/boards/test_board_id/lists",
        params={'key': 'test_key', 'token': 'test_token', 'name': 'NewList', 'pos': 'bottom'}
    )

@patch('src.trello.trello_api.TrelloClient.get_trello_list_id')
@patch('src.trello.trello_api.requests.post')
def test_add_card_to_trello_existing_list(mock_post, mock_get_trello_list_id, trello_client):
    mock_get_trello_list_id.return_value = 'list_id_12345'
    mock_post.return_value = MagicMock(status_code=200)
    mock_post.return_value.json.return_value = {'id': 'card_id_12345'}

    card = trello_client.add_card_to_trello('Test Card', 'TestList')
    assert card['id'] == 'card_id_12345'
    mock_get_trello_list_id.assert_called_once_with('TestList')
    mock_post.assert_called_once_with(
        f"{TRELLO_API_BASE}/cards",
        params={'key': 'test_key', 'token': 'test_token', 'idList': 'list_id_12345', 'name': 'Test Card', 'due': None}
    )

@patch('src.trello.trello_api.TrelloClient.get_trello_list_id')
@patch('src.trello.trello_api.TrelloClient.create_trello_list')
@patch('src.trello.trello_api.requests.post')
def test_add_card_to_trello_new_list(mock_post, mock_create_list, mock_get_list_id, trello_client):
    mock_get_list_id.return_value = None
    mock_create_list.return_value = 'new_list_id_67890'
    mock_post.return_value = MagicMock(status_code=200)
    mock_post.return_value.json.return_value = {'id': 'card_id_abcde'}

    card = trello_client.add_card_to_trello('Another Card', 'AnotherList')
    assert card['id'] == 'card_id_abcde'
    mock_get_list_id.assert_called_once_with('AnotherList')
    mock_create_list.assert_called_once_with('AnotherList')
    mock_post.assert_called_once_with(
        f"{TRELLO_API_BASE}/cards",
        params={'key': 'test_key', 'token': 'test_token', 'idList': 'new_list_id_67890', 'name': 'Another Card', 'due': None}
    )

@patch('src.trello.trello_api.TrelloClient.get_trello_list_id')
@patch('src.trello.trello_api.requests.get')
def test_get_trello_cards(mock_get, mock_get_list_id, trello_client):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'name': 'Task 1'}, {'name': 'Task 2'}]
    cards = trello_client.get_trello_cards('TestList')
    assert len(cards) == 2
    mock_get.assert_called_once()

@patch('src.trello.trello_api.TrelloClient.get_trello_list_id')
@patch('src.trello.trello_api.requests.get')
@patch('src.trello.trello_api.requests.delete')
def test_delete_card_from_trello(mock_delete, mock_get, mock_get_list_id, trello_client):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'id': 'card_id_12345', 'name': 'Test Card'}]
    mock_delete.return_value = MagicMock(status_code=200)
    card_id = trello_client.delete_card_from_trello('Test Card', 'TestList')
    assert card_id == 'card_id_12345'
    mock_delete.assert_called_once()

@patch('src.trello.trello_api.TrelloClient.get_trello_list_id')
@patch('src.trello.trello_api.requests.put')
def test_archive_trello_list(mock_put, mock_get_list_id, trello_client):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_put.return_value = MagicMock(status_code=200)
    success = trello_client.archive_trello_list('TestList')
    assert success is True
    mock_put.assert_called_once()