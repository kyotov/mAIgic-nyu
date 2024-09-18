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

## License
### MIT License

Copyright (c) 2024 Satyam Chatrola

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
