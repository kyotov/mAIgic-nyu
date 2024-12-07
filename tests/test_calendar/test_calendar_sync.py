# tests/test_calendar/test_calendar_sync.py

import pytest
from unittest.mock import patch
from src.calendar.calendar_sync import (
    add_task_to_calendar,
    update_task_in_calendar,
    delete_task_from_calendar,
)

@patch('src.calendar.calendar_sync.add_event_to_calendar')
def test_add_task_to_calendar(mock_add_event):
    mock_add_event.return_value = 'event_id_12345'
    event_id = add_task_to_calendar('Test Task', '2023-12-31T23:59:00-05:00')
    mock_add_event.assert_called_once_with('Test Task', '2023-12-31T23:59:00-05:00')
    assert event_id == 'event_id_12345'

def test_add_task_to_calendar_no_due_date():
    event_id = add_task_to_calendar('Test Task', None)
    assert event_id is None

@patch('src.calendar.calendar_sync.update_calendar_event')
def test_update_task_in_calendar(mock_update_event):
    update_task_in_calendar('event_id_12345', 'Updated Task', '2024-01-01T00:00:00-05:00')
    mock_update_event.assert_called_once_with('event_id_12345', 'Updated Task', '2024-01-01T00:00:00-05:00')

@patch('src.calendar.calendar_sync.delete_calendar_event')
def test_delete_task_from_calendar(mock_delete_event):
    delete_task_from_calendar('event_id_12345')
    mock_delete_event.assert_called_once_with('event_id_12345')