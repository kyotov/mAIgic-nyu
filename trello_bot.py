import os
import requests
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv
import re
from datetime import datetime
import threading
import gmail_bot  # Import the Gmail bot module
import calendar_sync
from pytz import timezone

# Load environment variables from .env file
load_dotenv()

# Start Gmail to Slack communication in a separate thread
# gmail_thread = threading.Thread(target=gmail_bot.run_gmail_to_slack)
# gmail_thread.start()

# Environment variables
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

# Set your local timezone, e.g., 'America/New_York' or 'Asia/Kolkata'
LOCAL_TIMEZONE = timezone("America/New_York")

# Initialize the Slack app (Bolt framework)
app = App(token=SLACK_BOT_TOKEN)

# Temporary dictionary to store the Trello card to Google Calendar event ID mapping
card_event_map = {}

# Fetch or create a Trello list ID for a specified list name
def get_or_create_trello_list_id(list_name):
    url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        lists = response.json()
        for lst in lists:
            if lst['name'].lower() == list_name.lower():
                return lst['id']
        # If list not found, create it
        create_list_url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'name': list_name,
            'pos': 'bottom'
        }
        create_response = requests.post(create_list_url, params=query)
        if create_response.status_code == 200:
            return create_response.json()['id']
        else:
            raise Exception(f"Failed to create list {list_name}: {create_response.status_code}, {create_response.text}")
    else:
        raise Exception(f"Failed to fetch lists from Trello: {response.status_code}, {response.text}")

# Add a card to a specified list in Trello with an optional due date
def add_card_to_trello(card_name, list_name, due_date=None):
    list_id = get_or_create_trello_list_id(list_name)
    url = f"https://api.trello.com/1/cards"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': card_name,
        'due': due_date  # Add due date to the query parameters
    }
    response = requests.post(url, params=query)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add card to Trello: {response.status_code}, {response.text}")

# Fetch Trello cards from a specified list
def get_trello_cards(list_name):
    list_id = get_or_create_trello_list_id(list_name)
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        cards = response.json()
        tasks = [card['name'] for card in cards]
        return tasks
    else:
        raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

# Post a message to Slack channel
def post_to_slack(channel, message):
    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    response = slack_client.chat_postMessage(channel=channel, text=message)
    return response

# Handle "add" message in Slack to add a task to a specified list with an optional due date
@app.message(re.compile(r'add "(.*)" to (.*?)(?: by (\d{4}-\d{2}-\d{2} \d{2}:\d{2}))?$'))
def add_to_trello_task(message, say, context):
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
            response_message = f"Added '{task_to_add}' to '{list_name}' with a due date of {due_date_str}. Event ID: {event_id} added to Google Calendar."
        else:
            response_message = f"Added '{task_to_add}' to '{list_name}'."
    except Exception as e:
        response_message = f"Failed to add the task. Error: {e}"
    
    post_to_slack(message['channel'], response_message)

# Delete a card from a specified list in Trello and remove from Google Calendar
def delete_card_from_trello(card_name, list_name):
    list_id = get_or_create_trello_list_id(list_name)
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            if card['name'].lower() == card_name.lower():
                card_id = card['id']
                delete_url = f"https://api.trello.com/1/cards/{card_id}?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
                delete_response = requests.delete(delete_url)
                
                if delete_response.status_code == 200:
                    if card_id in card_event_map:
                        event_id = card_event_map.pop(card_id)
                        delete_task_from_calendar(event_id)
                    return f"Deleted '{card_name}' from your Trello '{list_name}' list and corresponding Google Calendar event."
                else:
                    raise Exception(f"Failed to delete card: {delete_response.status_code}, {delete_response.text}")
        return f"No task found with the name '{card_name}' in your Trello '{list_name}' list."
    else:
        raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

# Handle "remove" message in Slack to delete a task from a specified Trello list
@app.message(re.compile(r'remove "(.*)" from (.*)'))
def remove_from_trello_task(message, say, context):
    task_to_remove = context['matches'][0]
    list_name = context['matches'][1]
    try:
        response_message = delete_card_from_trello(task_to_remove, list_name)
    except Exception as e:
        response_message = f"Failed to remove the task. Error: {e}"
    
    post_to_slack(message['channel'], response_message)

# Archive a Trello list by its name and delete associated calendar events
def archive_trello_list(list_name):
    list_id = get_or_create_trello_list_id(list_name)
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            card_id = card['id']
            if card_id in card_event_map:
                event_id = card_event_map.pop(card_id)
                delete_task_from_calendar(event_id)

    url = f"https://api.trello.com/1/lists/{list_id}/closed"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'value': 'true'
    }
    response = requests.put(url, params=query)

    if response.status_code == 200:
        return f"Archived the list '{list_name}' in Trello and removed associated Google Calendar events."
    else:
        raise Exception(f"Failed to archive the list '{list_name}': {response.status_code}, {response.text}")

# Handle "delete list" message in Slack to archive a Trello list
@app.message(re.compile(r'delete list (.*)'))
def delete_trello_list(message, say, context):
    list_name = context['matches'][0]
    try:
        response_message = archive_trello_list(list_name)
    except Exception as e:
        response_message = f"Failed to delete the list. Error: {e}"
    
    post_to_slack(message['channel'], response_message)

# Function to handle task addition with due date
def add_task_to_calendar(task_name, due_date):
    if due_date:
        event_id = calendar_sync.add_event_to_calendar(task_name, due_date)
        return event_id
    return None

# Function to handle task update with a new due date
def update_task_in_calendar(event_id, task_name, new_due_date):
    if new_due_date:
        calendar_sync.update_calendar_event(event_id, task_name, new_due_date)

# Function to handle task deletion
def delete_task_from_calendar(event_id):
    calendar_sync.delete_calendar_event(event_id)

# Handle "delete list" message in Slack to archive a Trello list
@app.message(re.compile(r'delete list (.*)'))
def delete_trello_list(message, say, context):
    # Extract the list name from the message
    list_name = context['matches'][0]
    
    # Archive the list in Trello
    try:
        response_message = archive_trello_list(list_name)
    except Exception as e:
        response_message = f"Failed to delete the list. Error: {e}"
    
    # Post the result back to Slack
    post_to_slack(message['channel'], response_message)

@app.message("fetch emails")
def handle_fetch_emails(message, say):
    say("Fetching the latest 5 unread emails...")
    gmail_bot.fetch_and_post_emails()


# Handle "show me tasks in" message in Slack to fetch tasks from a specified Trello list
@app.message(re.compile(r'show me tasks in (.*)'))
def show_tasks_in_list(message, say, context):
    # Extract the list name from the message
    list_name = context['matches'][0]
    
    # Fetch tasks from Trello
    try:
        tasks = get_trello_cards(list_name)
        if tasks:
            task_list = "\n".join(tasks)
            response_message = f"Here are the tasks in '{list_name}':\n{task_list}"
        else:
            response_message = f"No tasks found in '{list_name}'."
    except Exception as e:
        response_message = f"Failed to fetch tasks. Error: {e}"
    
    # Post the result back to Slack
    post_to_slack(message['channel'], response_message)

# Handle "show me X emails" command in Slack
@app.message(re.compile(r'show me (\d+) emails'))
def handle_show_emails(message, say, context):
    # Extract the number of emails requested from the message
    num_emails = int(context['matches'][0])
    
    # Send a message to confirm the request
    say(f"Fetching the latest {num_emails} unread emails...")
    
    # Call fetch_and_post_emails with the specified number of emails
    gmail_bot.fetch_and_post_emails(num_emails)

# Manual command to fetch emails
@app.message("fetch emails")
def handle_fetch_emails(message, say):
    say("Fetching the latest 5 unread emails...")
    gmail_bot.fetch_and_post_emails()


# Handle "help" message in Slack to show available commands
@app.message("help")
def show_help(message, say):
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
    # Post the help message to Slack
    post_to_slack(message['channel'], help_text)


# Start the Slack Bolt app (to listen for events using Socket Mode)
if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
