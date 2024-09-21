import json
from pprint import pformat, pprint
from typing import Any
from src.db.models import DB, Item, ItemType
from src.gmail.client import Gmail
from src.gmail.models import GMailMessage
import logging

from src.gpt.gpt import GPT, Line, Role
from src.slack.slack import Slack

LOGGER = logging.getLogger(__file__)


class Assistant:
    def __init__(self) -> None:
        # self.db = DB()
        # self.gpt = GPT()
        pass

    def fetch_emails(self) -> int:
        try:
            gmail = Gmail()
            db = DB()
            new_count = 0
            # TODO(kamen): figure out how to query for new emails only?
            #   maybe based on date of the last email we know about?
            #   just ask for emails that are newer than that date?
            for message in gmail.query():
                if (
                    found := db.session.query(Item)
                    .where((Item.type == ItemType.gmail) & (Item.id == message["id"]))
                    .first()
                ):
                    LOGGER.debug("skipping %s already in database", found.id)
                else:
                    mm = gmail.get_message(message["id"])
                    m = GMailMessage(mm)
                    db.session.add(
                        Item(type=ItemType.gmail, id=mm["id"], content=m.as_md())
                    )
                    db.session.commit()
                    LOGGER.debug("added %s to database", mm["id"])
                    new_count += 1
            return new_count
        except Exception as e:
            LOGGER.exception("fetch_emails failed")
            raise

    def handle_new_email(self, item: Item) -> dict[str, Any]:
        gpt = GPT()
        lines = [
            Line(
                role=Role.SYSTEM,
                content="""
                    I am Kamen Yotov.
                    My emails are kamen@yotov.org, kyotov@gmail.com, ky12@nyu.edu.
                    
                    When I receive an email, I want you to analyze it as follows and respond in json.

                    Since you are the first to see the email you have to present it to me as news.

                    * "author"
                    * "time_received" in iso format
                    * "categories"
                        ** "urgent": bool
                        ** "important": bool
                        ** "spam": bool
                    * "summary" : summary of the content
                    * "action": proposed next action
                 """,
            ),
            Line(role=Role.USER, content=item.content),
        ]
        r = gpt.complete(lines)
        assert len(r.choices) == 1
        assert r.choices[0].finish_reason == "stop"
        result = r.choices[0].message.content
        LOGGER.info(pformat(result))
        result = result.removeprefix("```json").removesuffix("```")
        result = json.loads(result)
        result["id"] = item.id
        LOGGER.info(pformat(result))
        return result

    def handle_one(self) -> dict[str, Any]:
        db = DB()
        if new_item := db.session.query(Item).where(Item.slack_thread.is_(None)).first():
            LOGGER.info("handling %s", new_item.id)
            return self.handle_new_email(new_item)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    a = Assistant()
    a.fetch_emails()
    a.handle_one()
