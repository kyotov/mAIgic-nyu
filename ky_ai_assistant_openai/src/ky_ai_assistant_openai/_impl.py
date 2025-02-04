import enum
from dataclasses import dataclass
import logging

import openai

import ky_ai_assistant_api


_LOGGER = logging.getLogger(__name__)


class Role(enum.StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class Message:
    role: Role
    content: str


class Thread(ky_ai_assistant_api.Thread):
    def __init__(self, client: "Client", message: str):
        self._client = client
        self._history = [Message(Role.SYSTEM, message)]

    def post(self, message: str) -> str:
        self._history.append(Message(Role.USER, message))
        response = self._client.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": x.role, "content": x.content} for x in self._history],
        )
        _LOGGER.debug("Response: %s", response)
        self._history.append(
            Message(Role.ASSISTANT, response.choices[0].message.content)
        )
        return self._history[-1].content


class Client(ky_ai_assistant_api.Client):
    def __init__(self):
        self.client = openai.OpenAI()

    def new_thread(self, message: str) -> Thread:
        return Thread(self, message)


def get_client() -> Client:
    return Client()
