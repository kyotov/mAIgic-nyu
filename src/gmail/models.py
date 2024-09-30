import base64
from pprint import pprint
from typing import Any, ClassVar
from html2text import html2text
from pydantic import BaseModel


class Header(BaseModel):
    name: str
    value: str


class GmailMessagePart:
    interesting_header_names: ClassVar[set[str]] = {
        "From",
        "To",
        "Date",
        "Subject",
    }

    def __init__(self, part: dict[str, Any]) -> None:
        self._part = part

    @property
    def headers(self) -> list[Header]:
        return [
            Header(name=x["name"], value=x["value"])
            for x in self._part["headers"]
            if x["name"] in self.interesting_header_names
        ]

    @property
    def body(self) -> str:
        # TODO(kamen): sometimes there is no body... 
        #   e.g. there maybe `attachmentId` instead.
        #   we are not handling that for now... :(
        if self._part["body"]["size"] != 0 and "data" in self._part["body"]:
            try:
                data = self._part["body"]["data"]
                decoded = base64.urlsafe_b64decode(data).decode()
                if "<html" in decoded:
                    decoded = html2text(decoded)
                return decoded
            except Exception as e:
                pprint(self._part["body"])
                raise
        return ""

    @property
    def parts(self) -> list["GmailMessagePart"]:
        return [__class__(x) for x in self._part.get("parts", [])]

    def as_dict(self) -> dict[str, Any]:
        return dict(
            headers=[x.model_dump() for x in self.headers],
            body=self.body,
            parts=[x.as_dict() for x in self.parts],
        )
    
    def as_md(self) -> str:
        result = []
        result.append("-" * 80)
        for header in self.headers:
            result.append(f"{header.name}: {header.value}")
        result.append("")
        result.append(self.body)
        for part in self.parts:
            result.append(part.as_md())
        return "\n".join(result)


class GMailMessage:
    def __init__(self, message: dict[str, Any]) -> None:
        self._message = message

    @property
    def label_ids(self) -> list[str]:
        return self._message["labelIds"]

    @property
    def thread_id(self) -> str:
        return self._message["threadId"]

    @property
    def parts(self) -> list[GmailMessagePart]:
        return [GmailMessagePart(self._message["payload"])] + [
            GmailMessagePart(x) for x in self._message.get("parts", [])
        ]

    def as_dict(self) -> dict[str, Any]:
        return dict(
            label_ids=self.label_ids,
            thread_id=self.thread_id,
            parts=[x.as_dict() for x in self.parts],
        )

    def as_md(self) -> str:
        result = []
        result.append(f"labels: {', '.join(self.label_ids)}")
        result.append(f"thread: {self.thread_id}")
        for part in self.parts:
            result.append(part.as_md())
        return "\n".join(result)


