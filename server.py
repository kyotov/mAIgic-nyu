import asyncio
from datetime import datetime
import enum
import logging
import os
from concurrent.futures import Future, ProcessPoolExecutor
from pprint import pformat
from queue import Queue
from typing import TypeVar

from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp

from assistant import Assistant
from src.db.models import DB, Item

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__file__)

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])


class OP(enum.Enum):
    fetch = enum.auto()
    handle_one = enum.auto()


T = TypeVar("T")


class Server:
    pool: ProcessPoolExecutor

    def __init__(self) -> None:
        self.assistant = Assistant()
        app.message()(self.message_hello)

        self.queue = Queue()

    async def await_future(self, future: Future[T]) -> T:
        done = asyncio.Event()
        future.add_done_callback(lambda _: done.set())
        await done.wait()
        return future.result()

    async def _slack_app(self):
        handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        await handler.start_async()

    def run(self):
        with ProcessPoolExecutor() as pool:
            self.pool = pool
            asyncio.run(self._slack_app())

    async def message_hello(self, message, ack):
        await ack()
        match message["text"]:

            case str(value) if "fetch" in value:
                future = self.pool.submit(self.assistant.fetch_emails)
                found = await self.await_future(future)
                LOGGER.info("%s new emails found", found)

            case str(value) if "handle_one" in value:
                future = self.pool.submit(self.assistant.handle_one)
                result = await self.await_future(future)

                time = datetime.fromisoformat(result["time_received"])

                r = await app.client.chat_postMessage(
                    channel=os.getenv("SLACK_CHANNEL_ID"),
                    text=f"Handling `{result['id']}`...",
                    unfurl_links=False,
                    unfurl_media=False,
                )
                r.validate()
                ts = r.get("ts")

                r = await app.client.chat_update(
                    channel=os.getenv("SLACK_CHANNEL_ID"),
                    ts=ts,
                    blocks=[
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"`From:` {result['author']}",
                                },
                            ],
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"`When:` <https://mail.google.com/mail/u/0/#inbox/{result['id']}|{time}>",
                                },
                            ],
                        },
                        {"type": "divider"},
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"{result['summary']}",
                                },
                            ],
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"{result['action']}",
                                },
                            ],
                        },
                    ],
                )
                r.validate()

                db = DB()
                item = db.session.query(Item).where(Item.id == result["id"]).one()
                item.slack_channel = "C01CAH729TK"
                item.slack_thread = r.get("ts")
                db.session.commit()

                LOGGER.info(pformat(r.data))

        LOGGER.info("\n" + pformat(message))


if __name__ == "__main__":
    Server().run()

# https://mail.google.com/mail/u/0/#inbox/19245a9bd60a75f6
