import base64
import os
from functools import cache
from pprint import pformat
from typing import ClassVar, Iterator

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from html2text import html2text
import ky_mail_api


class _MessagePart:
    """A part of multi-part message.

    This is wrappiong https://developers.google.com/gmail/api/reference/rest/v1/users.messages#Message.MessagePart

    TODO(kamen): currently we don't parse attachments.
        My preliminary research shows that attachments are in `multipart/mixed` parts.
        One day we will get to them...
    """

    def __init__(self, client: "Client", data: dict):
        self._client = client
        self._data = data

    @property
    def id(self) -> str:
        return self._data["partId"]

    @property
    def mime_type(self) -> str:
        return self._data["mimeType"]

    @property
    def filename(self) -> str | None:
        return self._data.get("filename")

    @property
    @cache
    def headers(self) -> dict[str, str]:
        """Return the headers of the message.

        Create a dictionary of headers and cache the result.

        TODO(kamen): This may "eat" headers if multiple headers have the same name!!!
                        Check if this is possible and if so, how to handle it.
        """

        return {h["name"]: h["value"] for h in self._data.get("headers", [])}

    @property
    def body(self) -> str:
        # FIXME(kamen): eventually support attachments
        assert self._data.get("attachmentId") is None

        data = self._data["body"].get("data", "")
        data = base64.urlsafe_b64decode(data).decode()

        return data

    @property
    def parts(self) -> Iterator["_MessagePart"]:
        for part in self._data.get("parts", []):
            yield _MessagePart(self._client, part)

    def as_dict(
        self,
        no_body: bool = False,
        header_keys_only: bool = False,
    ) -> dict[str, str]:
        return {
            "id": self.id,
            "mime_type": self.mime_type,
            "filename": self.filename,
            "headers": [
                key if header_keys_only else (key, value)
                for key, value in self.headers.items()
            ],
            "body": "..." if no_body else self.body,
            "parts": [
                x.as_dict(no_body=no_body, header_keys_only=header_keys_only)
                for x in self.parts
            ],
        }

    def __str__(self) -> str:
        return pformat(self.as_dict(no_body=True, header_keys_only=True), indent=2)


class Message(ky_mail_api.Message):
    def __init__(self, client: "Client", data: dict):
        self._client = client
        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def from_(self) -> str:
        return self._payload.headers["From"]

    @property
    def to(self) -> str:
        return self._payload.headers["To"]

    @property
    def date(self) -> str:
        return self._payload.headers["Date"]

    @property
    def subject(self) -> str:
        return self._payload.headers["Subject"]

    @property
    def body(self) -> str:
        return self._extract_body(self._payload)

    def _extract_body(self, part: _MessagePart) -> str:
        match part.mime_type:
            case "text/plain":
                return self._cleanup_body(part.body)

            case "text/html":
                return self._cleanup_body(html2text(part.body))

            case "multipart/alternative":
                for p in part.parts:
                    if p.mime_type in ("text/plain", "text/html"):
                        return self._cleanup_body(p.body)

            case "multipart/mixed":
                for p in part.parts:
                    if p.mime_type in ("multipart/alternative", "text/html"):
                        return self._extract_body(p)

        # if we end up here, we did not find an altenative we know how to parse!!!
        m = f"{part.mime_type}: cannot parse any of {[p.mime_type for p in part.parts]}"
        raise RuntimeError(m)

    def _cleanup_body(self, body: str) -> str:
        t = body.split("\n")
        t = [x.strip() for x in t]
        t = "\n".join(t)
        t = t.replace("\n\n", "\n")
        return t

    @property
    @cache
    def _payload(self) -> _MessagePart:
        content = (
            self._client._service.users()
            .messages()
            .get(userId="me", id=self.id)
            .execute()
        )
        return _MessagePart(self._client, content["payload"])


class Client(ky_mail_api.Client):
    SCOPES: ClassVar[list[str]] = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self):
        creds = self._authenticate()
        self._service = build("gmail", "v1", credentials=creds)

    def get_messages(self) -> Iterator[Message]:
        # FIXME(kamen): this is currently restricted to inbox...
        #   ideally we should provide a way to be more generic.

        results = (
            self._service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX"])
            .execute()
        )

        while True:
            for message in results["messages"]:
                yield Message(self, message)

            if next_token := results.get("nextPageToken"):
                results = (
                    self._service.users()
                    .messages()
                    .list(userId="me", labelIds=["INBOX"], pageToken=next_token)
                    .execute()
                )
            else:
                break

    def _authenticate(self):
        # FIXME(kamen): abstract away the `token.json` name

        # try to retrieve previously stored credentials
        #
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        # if expired credentials are found, refresh them
        #
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # if we still don't have valid credentials (or none at all), authenticate
        #
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", self.SCOPES
            )
            creds = flow.run_local_server(port=0)

        # store the credentials for future use
        #
        with open("token.json", "w") as token:
            token.write(creds.to_json())

        return creds
