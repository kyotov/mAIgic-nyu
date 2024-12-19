# mAIgic

## Project Description

**mAIgic** is an AI-powered assistant designed to enhance productivity and organization by tracking messages and important information across multiple platforms. It identifies and reminds users about follow-ups, ensuring timely responses and efficient information management. With intelligent search capabilities, mAIgic enables users to easily locate conversations and details tied to specific individuals or tasks.

The project supports popular platforms such as Slack, Trello, Gmail, and Google Calendar, providing seamless follow-up tracking, reminders, and contextual search across these communication channels. This integration leverages AI to automate the reminder process, making it easier to stay on top of essential follow-ups and tasks.

## Features

- **Slack Integration**: Manage tasks, create checklists, and fetch emails directly from Slack.
- **Trello Integration**: Automate task management with Trello boards, lists, and cards.
- **Gmail Integration**: Fetch and post unread emails to Slack channels.
- **Google Calendar Integration**: Automatically synchronize tasks with due dates to Google Calendar.
- **Unit Testing**: Comprehensive test coverage using `pytest`.
- **Static Code Analysis**: Ensure code quality with `ruff` (linter).
- **Type Checking**: Maintain type consistency with `mypy`.
- **Continuous Integration**: CircleCI pipeline for running tests and static analysis on every push.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mAIgic.git
cd mAIgic
```

### 2. Install Dependencies

Using the uv package manager, run the following command:

```bash
uv sync
```

This will install all required dependencies in a virtual environment. To activate the virtual environment:

```bash
source ./.venv/bin/activate
```

## Running the Application

### 1. Start the Application

Run the application to start the Slack bot and Gmail bot:

```bash
python app.py
```

This will:
1. Start a thread for the Gmail bot to periodically fetch unread emails.
2. Initialize the Slack bot to listen for commands.

## Commands Overview

### Slack Commands

1. **Add Task to Trello**:
   ```
   add "task name" to [list name] by YYYY-MM-DD HH:MM
   ```
   - Adds a task to the specified Trello list.
   - If a due date is provided, it creates a Google Calendar event.

2. **Remove Task from Trello**:
   ```
   remove "task name" from [list name]
   ```
   - Removes a task from the Trello list and deletes the corresponding Google Calendar event.

3. **Show Tasks in Trello List**:
   ```
   show me tasks in [list name]
   ```
   - Displays all tasks in the specified Trello list.

4. **Delete Trello List**:
   ```
   delete list [list name]
   ```
   - Archives the specified Trello list and removes associated Google Calendar events.

5. **Fetch Unread Emails**:
   ```
   fetch emails
   ```
   - Fetches the latest 5 unread emails and posts them in Slack.

6. **Show Specific Number of Emails**:
   ```
   show me [number] emails
   ```
   - Fetches the specified number of unread emails.

7. **Create Checklist in Trello Card**:
   ```
   create checklist "checklist name" in "card name" in [list name]
   ```

8. **Add Item to Checklist**:
   ```
   add "item name" to checklist "checklist name" in "card name" in [list name]
   ```

9. **Help**:
   ```
   help
   ```
   - Displays the list of available commands.

## Running Tests

### Unit Tests

Run tests using pytest:

```bash
pytest tests
```

### Static Code Analysis

Check for linting issues with ruff:

```bash
ruff check .
```

### Type Checking

Perform type checking with mypy:

```bash
mypy .
```

## CircleCI Configuration

The project uses CircleCI for continuous integration. Every push triggers the following steps:
1. Install dependencies using uv.
2. Run unit tests using pytest.
3. Perform static code analysis using ruff.
4. Perform type checking using mypy.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributors

- Siddharth Singh - sms10221@nyu.edu
- Adittya Mittal - am14079@nyu.edu
- Anushka Tawte - at5849@nyu.edu
- Rafael de Leon - rdl404@nyu.edu
- Alex Ying - aty2009@nyu.edu
- Mridul Mittal - mm13171@nyu.edu