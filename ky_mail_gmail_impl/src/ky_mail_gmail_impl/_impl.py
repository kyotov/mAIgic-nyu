import os
from pprint import pformat
from typing import ClassVar, Iterator
import ky_mail_api

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Message(ky_mail_api.Message):
    def __init__(self, message: dict):
        self._message = message

    def get_body(self) -> str:
        # TODO(kamen): this does not yet return the body.

        m = self._message
        return pformat(m)


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
                yield Message(message)

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


# Dependency Injection of this implementation into the API
#
ky_mail_api.get_client = lambda: Client()
