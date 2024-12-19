# src/calendar/calendar_sync.py

from .calendar_api import add_event_to_calendar, update_calendar_event, delete_calendar_event

# Function to handle task addition with due date
def add_task_to_calendar(task_name: str, due_date: str) -> str:
    """
    Add a task to the Google Calendar if a due date is provided.

    Args:
        task_name (str): The name or summary of the task.
        due_date (str): The due date and time of the task in ISO 8601 format 
                        (e.g., '2024-12-04T10:00:00-07:00').

    Returns:
        str: The unique event ID of the created calendar event, or None if no due date is provided.

    Raises:
        googleapiclient.errors.HttpError: If the event creation fails.
    """
    if due_date:
        event_id = add_event_to_calendar(task_name, due_date)
        return event_id
    return None

# Function to handle task update with a new due date
def update_task_in_calendar(event_id: str, task_name: str, new_due_date: str) -> None:
    """
    Update an existing task in the Google Calendar with a new name or due date.

    Args:
        event_id (str): The unique ID of the calendar event to be updated.
        task_name (str): The updated name or summary of the task.
        new_due_date (str): The updated due date and time in ISO 8601 format.

    Returns:
        None

    Raises:
        googleapiclient.errors.HttpError: If the event update fails.
    """
    if new_due_date:
        update_calendar_event(event_id, task_name, new_due_date)

# Function to handle task deletion
def delete_task_from_calendar(event_id: str) -> None:
    """
    Delete a task from the Google Calendar.

    Args:
        event_id (str): The unique ID of the calendar event to be deleted.

    Returns:
        None

    Raises:
        googleapiclient.errors.HttpError: If the event deletion fails.
    """
    delete_calendar_event(event_id)