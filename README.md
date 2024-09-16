# mAIgic
This project will organize life by tracking messages and information that need follow-ups and reminding the user to take follow-ups. It will also provide a search based on individuals.

The project aims to leverage AI to track and remind for follow up messages for systems like Slack, Trello, Whatsapp, Gmail, Google Docs comments, etc.

# Technical tools
- Programming Language: Python
- Project dependency management tool: uv
- Project linter: ruff
- Project tester: pytest
- Continuous Integration (CI): circleCI

# Instructions
## Setup
- Install `uv` on your system with command with `curl -LsSf https://astral.sh/uv/install.sh | sh`.
- `cd` into the cloned repository and execute `uv sync` (This will install all the dependencies).
- Activate the environment `venv` by executing `source ./.venv/bin/activate`.

## Processes
- To check the formatting standard with ruff (linter) execute either `uv run ruff check .` or `ruff check .` from the root directory of the project.
- To test the code, execute either `uv run pytest .` or `pytest .` from the root directory of the project.

Note: One can run tools like ruff and pytest independently or can run them through `uv`.