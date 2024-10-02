import os

from slack_sdk import WebClient


class Slack:
    def __init__(self) -> None:
        client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

    def send(self, thread: str | None, text: str) -> None:
        r = self.client.chat_postMessage(
            channel="C01CAH729TK",
            thread=thread,
            text=text,
        )
        r.validate()
        return r
