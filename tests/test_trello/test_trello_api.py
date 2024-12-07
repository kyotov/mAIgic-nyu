# tests/test_trello/test_trello_api.py

import pytest
from unittest.mock import patch, MagicMock
from src.trello.trello_api import (
    get_or_create_trello_list_id,
    add_card_to_trello,
    get_trello_cards,
    delete_card_from_trello,
    archive_trello_list,
)

@patch('src.trello.trello_api.requests.get')
@patch('src.trello.trello_api.requests.post')
def test_get_or_create_trello_list_id_existing(mock_post, mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'id': 'list_id_12345', 'name': 'TestList'}]
    list_id = get_or_create_trello_list_id('TestList')
    assert list_id == 'list_id_12345'
    mock_post.assert_not_called()

@patch('src.trello.trello_api.requests.get')
@patch('src.trello.trello_api.requests.post')
def test_get_or_create_trello_list_id_new(mock_post, mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = []
    mock_post.return_value = MagicMock(status_code=200)
    mock_post.return_value.json.return_value = {'id': 'new_list_id_67890'}
    list_id = get_or_create_trello_list_id('NewList')
    assert list_id == 'new_list_id_67890'
    mock_post.assert_called_once()

@patch('src.trello.trello_api.get_or_create_trello_list_id')
@patch('src.trello.trello_api.requests.post')
def test_add_card_to_trello(mock_post, mock_get_list_id):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_post.return_value = MagicMock(status_code=200)
    mock_post.return_value.json.return_value = {'id': 'card_id_12345'}
    card = add_card_to_trello('Test Card', 'TestList')
    assert card['id'] == 'card_id_12345'
    mock_post.assert_called_once()

@patch('src.trello.trello_api.get_or_create_trello_list_id')
@patch('src.trello.trello_api.requests.get')
def test_get_trello_cards(mock_get, mock_get_list_id):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'name': 'Task 1'}, {'name': 'Task 2'}]
    cards = get_trello_cards('TestList')
    assert len(cards) == 2
    mock_get.assert_called_once()

@patch('src.trello.trello_api.get_or_create_trello_list_id')
@patch('src.trello.trello_api.requests.get')
@patch('src.trello.trello_api.requests.delete')
def test_delete_card_from_trello(mock_delete, mock_get, mock_get_list_id):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_get.return_value = MagicMock(status_code=200)
    mock_get.return_value.json.return_value = [{'id': 'card_id_12345', 'name': 'Test Card'}]
    mock_delete.return_value = MagicMock(status_code=200)
    card_id = delete_card_from_trello('Test Card', 'TestList')
    assert card_id == 'card_id_12345'
    mock_delete.assert_called_once()

@patch('src.trello.trello_api.get_or_create_trello_list_id')
@patch('src.trello.trello_api.requests.put')
def test_archive_trello_list(mock_put, mock_get_list_id):
    mock_get_list_id.return_value = 'list_id_12345'
    mock_put.return_value = MagicMock(status_code=200)
    success = archive_trello_list('TestList')
    assert success is True
    mock_put.assert_called_once()