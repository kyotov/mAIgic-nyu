# src/slack/slack_bot.py

import os
import re
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
from slack_bolt import Ack

from ..trello.trello_api import add_card_to_trello, get_trello_cards, delete_card_from_trello, archive_trello_list, get_card_id, create_checklist_in_card, get_checklist_id, add_item_to_checklist
from ..trello.trello_bot import card_event_map
from ..calendar.calendar_sync import add_task_to_calendar, delete_task_from_calendar
from ..gmail.gmail_bot import fetch_and_post_emails
from .slack_api import post_to_slack

# Load environment variables from .env file
load_dotenv()

# Environment variables
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
LOCAL_TIMEZONE = timezone("America/New_York")  # Adjust as necessary

# Initialize the Slack app (Bolt framework)
app = App(token=SLACK_BOT_TOKEN)

# Handle "add" message in Slack to add a task to a specified list with an optional due date
@app.message(re.compile(r'add "(.*)" to (.*?)(?: by (\d{4}-\d{2}-\d{2} \d{2}:\d{2}))?$'))
def add_to_trello_task(message, say, context):
    """
    Handle the "add" command to add a task to a Trello list with an optional due date.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.
        context: Context object containing matched regex groups.

    Returns:
        None
    """
    task_to_add = context['matches'][0]
    list_name = context['matches'][1]
    due_date_str = context['matches'][2] if len(context['matches']) > 2 else None

    due_date = None
    if due_date_str:
        try:
            naive_due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
            local_due_date = LOCAL_TIMEZONE.localize(naive_due_date)
            due_date = local_due_date.isoformat()
        except ValueError:
            response_message = "Failed to add the task. Please provide date and time in 'YYYY-MM-DD HH:MM' format."
            post_to_slack(message['channel'], response_message)
            return

    try:
        added_card = add_card_to_trello(task_to_add, list_name, due_date)
        if due_date:
            event_id = add_task_to_calendar(task_to_add, due_date)
            card_id = added_card['id']
            card_event_map[card_id] = event_id
            response_message = f"Added '{task_to_add}' to '{list_name}' with a due date of {due_date_str}. Event added to Google Calendar."
        else:
            response_message = f"Added '{task_to_add}' to '{list_name}'."
    except Exception as e:
        response_message = f"Failed to add the task. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handle "remove" message in Slack to delete a task from a specified Trello list
@app.message(re.compile(r'remove "(.*)" from (.*)'))
def remove_from_trello_task(message, say, context):
    """
    Handle the "remove" command to delete a task from a Trello list.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.
        context: Context object containing matched regex groups.

    Returns:
        None
    """
    task_to_remove = context['matches'][0]
    list_name = context['matches'][1]
    try:
        card_id = delete_card_from_trello(task_to_remove, list_name)
        if card_id:
            if card_id in card_event_map:
                event_id = card_event_map.pop(card_id)
                delete_task_from_calendar(event_id)
            response_message = f"Deleted '{task_to_remove}' from your Trello '{list_name}' list and corresponding Google Calendar event."
        else:
            response_message = f"No task found with the name '{task_to_remove}' in your Trello '{list_name}' list."
    except Exception as e:
        response_message = f"Failed to remove the task. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handle "delete list" message in Slack to archive a Trello list
@app.message(re.compile(r'delete list (.*)', re.IGNORECASE))
def delete_trello_list(message, say, context):
    """
    Handle the "delete list" command to archive a Trello list.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.
        context: Context object containing matched regex groups.

    Returns:
        None
    """
    list_name = context['matches'][0]
    try:
        success = archive_trello_list(list_name)
        if success:
            # Also need to remove calendar events for tasks in this list
            try:
                cards = get_trello_cards(list_name)
                for card in cards:
                    card_id = card['id']
                    if card_id in card_event_map:
                        event_id = card_event_map.pop(card_id)
                        delete_task_from_calendar(event_id)
            except Exception as e:
                # Handle the case where the list was archived but cards couldn't be fetched
                pass  # You might want to log this error

            response_message = f"Archived the list '{list_name}' in Trello and removed associated Google Calendar events."
        else:
            response_message = f"The list '{list_name}' does not exist in Trello."
    except Exception as e:
        response_message = f"Failed to delete the list. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handle "show me tasks in" message in Slack to fetch tasks from a specified Trello list
@app.message(re.compile(r'show me tasks in (.*)'))
def show_tasks_in_list(message, say, context):
    """
    Handle the "show me tasks in" command to display tasks in a Trello list.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.
        context: Context object containing matched regex groups.

    Returns:
        None
    """
    list_name = context['matches'][0]

    try:
        cards = get_trello_cards(list_name)
        tasks = [card['name'] for card in cards]
        if tasks:
            task_list = "\n".join(tasks)
            response_message = f"Here are the tasks in '{list_name}':\n{task_list}"
        else:
            response_message = f"No tasks found in '{list_name}'."
    except Exception as e:
        response_message = f"Failed to fetch tasks. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handle "show me X emails" command in Slack
@app.message(re.compile(r'show me (\d+) emails'))
def handle_show_emails(message, say, context):
    """
    Handle the "show me X emails" command to fetch and post unread emails.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.
        context: Context object containing matched regex groups.

    Returns:
        None
    """
    num_emails = int(context['matches'][0])

    say(f"Fetching the latest {num_emails} unread emails...")

    fetch_and_post_emails(num_emails)

# Handle "fetch emails" command
@app.message("fetch emails")
def handle_fetch_emails(message, say):
    """
    Handle the "fetch emails" command to fetch the latest 5 unread emails.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.

    Returns:
        None
    """
    say("Fetching the latest 5 unread emails...")
    fetch_and_post_emails()

# Handler to create a checklist in a card
@app.message(re.compile(r'create checklist "(.*)" in "(.*)" in (.*)', re.IGNORECASE))
def create_checklist_handler(message, say, context):
    checklist_name = context['matches'][0]
    card_name = context['matches'][1]
    list_name = context['matches'][2]

    try:
        # Get card ID
        card_id = get_card_id(card_name, list_name)
        if card_id is None:
            response_message = f"The card '{card_name}' does not exist in list '{list_name}'."
            post_to_slack(message['channel'], response_message)
            return

        # Create checklist
        checklist = create_checklist_in_card(card_id, checklist_name)
        response_message = f"Created checklist '{checklist_name}' in card '{card_name}' in list '{list_name}'."
    except Exception as e:
        response_message = f"Failed to create checklist. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handler to add an item to a checklist
@app.message(re.compile(r'add "(.*)" to checklist "(.*)" in "(.*)" in (.*)', re.IGNORECASE))
def add_item_to_checklist_handler(message, say, context):
    item_name = context['matches'][0]
    checklist_name = context['matches'][1]
    card_name = context['matches'][2]
    list_name = context['matches'][3]

    try:
        # Get card ID
        card_id = get_card_id(card_name, list_name)
        if card_id is None:
            response_message = f"The card '{card_name}' does not exist in list '{list_name}'."
            post_to_slack(message['channel'], response_message)
            return

        # Get checklist ID
        checklist_id = get_checklist_id(card_id, checklist_name)
        if checklist_id is None:
            response_message = f"The checklist '{checklist_name}' does not exist in card '{card_name}'."
            post_to_slack(message['channel'], response_message)
            return

        # Add item to checklist
        item = add_item_to_checklist(checklist_id, item_name)
        response_message = f"Added item '{item_name}' to checklist '{checklist_name}' in card '{card_name}'."
    except Exception as e:
        response_message = f"Failed to add item to checklist. Error: {e}"

    post_to_slack(message['channel'], response_message)

# Handle "help" message in Slack to show available commands
@app.message("help")
def show_help(message, say):
    """
    Handle the "help" command to display a list of available Slack commands.

    Args:
        message: The incoming Slack message event.
        say: Function to respond to the user in Slack.

    Returns:
        None
    """
    help_text = """
Here are the commands you can use:

*Task Management Commands:*
1. **Add a task to a list**:
   `add "task name" to [list name] by YYYY-MM-DD HH:MM`
   - Adds a task to the specified list with an optional due date and time.
   - If a due date and time are provided, it will also create an event in Google Calendar.

2. **Remove a task from a list**:
   `remove "task name" from [list name]`
   - Deletes the specified task from the specified Trello list.
   - If the task has a corresponding Google Calendar event, it will also be deleted.

3. **Show tasks in a list**:
   `show me tasks in [list name]`
   - Displays all tasks in the specified Trello list.

4. **Delete (archive) a list**:
   `delete list [list name]`
   - Archives the specified Trello list, effectively removing it from the board.
   - If there are Google Calendar events associated with tasks in this list, they will also be deleted.

*Email Commands:*
5. **Fetch unread emails**:
   `fetch emails`
   - Fetches the latest 5 unread emails from Gmail and posts them in Slack.

6. **Show me X emails**:
   `show me [number] emails`
   - Fetches the specified number of unread emails from Gmail and posts them in Slack.
   - Example: `show me 10 emails`

*General Commands:*
7. **Help**:
   `help`
   - Displays this help message with all available commands.

*Google Calendar Synchronization*:
- When you add a task to a Trello list with a due date and time using the `add` command, a Google Calendar event is automatically created for that task.
- When you delete a task from a Trello list using the `remove` command, the corresponding Google Calendar event is also deleted if it exists.
- When you delete an entire Trello list using the `delete list` command, all Google Calendar events associated with tasks in that list are also removed.

*Note:* Make sure to use double quotes around task names when adding or removing specific tasks.
"""
    post_to_slack(message['channel'], help_text)

@app.event("message")
def handle_unhandled_messages(event, say, logger):
    user = event.get('user')
    text = event.get('text')
    logger.info(f"Unhandled message from user {user}: {text}")
    say(f"Sorry, I don't understand that command. Type `help` to see the list of available commands.")


# Expose the app for the main application
def run_slack_bot():
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    handler = SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN'))
    handler.start()

