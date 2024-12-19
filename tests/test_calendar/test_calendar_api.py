# tests/test_calendar/test_calendar_api.py

import pytest
from unittest.mock import patch, MagicMock
from src.calendar.calendar_api import (
    authenticate_google_calendar,
    add_event_to_calendar,
    update_calendar_event,
    delete_calendar_event,
)

# Mock the authenticate_google_calendar function to prevent actual authentication
@patch('src.calendar.calendar_api.authenticate_google_calendar')
def test_add_event_to_calendar(mock_authenticate):
    # Mock the credentials and service
    mock_authenticate.return_value = MagicMock()
    with patch('src.calendar.calendar_api.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_events = mock_service.events.return_value
        mock_insert = mock_events.insert.return_value
        mock_execute = mock_insert.execute.return_value
        mock_execute.get.return_value = 'event_id_12345'
        mock_execute.__getitem__.return_value = 'event_id_12345'

        # Call the function
        event_id = add_event_to_calendar('Test Task', '2023-12-31T23:59:00-05:00')

        # Assertions
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_authenticate.return_value)
        mock_service.events.assert_called_once()
        mock_events.insert.assert_called_once()
        mock_insert.execute.assert_called_once()
        assert event_id == 'event_id_12345'

@patch('src.calendar.calendar_api.authenticate_google_calendar')
def test_update_calendar_event(mock_authenticate):
    mock_authenticate.return_value = MagicMock()
    with patch('src.calendar.calendar_api.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_events = mock_service.events.return_value
        mock_get = mock_events.get.return_value
        mock_get.execute.return_value = {
            'id': 'event_id_12345',
            'summary': 'Old Task',
            'start': {'dateTime': '2023-12-31T23:59:00-05:00'},
            'end': {'dateTime': '2023-12-31T23:59:00-05:00'},
        }
        mock_update = mock_events.update.return_value
        mock_update.execute.return_value = {'updated': True}

        # Call the function
        updated_event = update_calendar_event('event_id_12345', 'Updated Task', '2024-01-01T00:00:00-05:00')

        # Assertions
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_authenticate.return_value)
        mock_events.get.assert_called_once_with(calendarId='primary', eventId='event_id_12345')
        mock_get.execute.assert_called_once()
        mock_events.update.assert_called_once()
        mock_update.execute.assert_called_once()
        assert updated_event == {'updated': True}

@patch('src.calendar.calendar_api.authenticate_google_calendar')
def test_delete_calendar_event(mock_authenticate):
    mock_authenticate.return_value = MagicMock()
    with patch('src.calendar.calendar_api.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_events = mock_service.events.return_value
        mock_delete = mock_events.delete.return_value
        mock_delete.execute.return_value = None

        # Call the function
        delete_calendar_event('event_id_12345')

        # Assertions
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_authenticate.return_value)
        mock_events.delete.assert_called_once_with(calendarId='primary', eventId='event_id_12345')
        mock_delete.execute.assert_called_once()