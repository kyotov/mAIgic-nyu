from typing import Iterator, Protocol


class Message(Protocol):
    """A Mail Message."""

    def get_body(self) -> str:
        """Return the body of the message."""

        raise NotImplementedError()


class Client(Protocol):
    """A Mail Client used to fetch messages."""

    def get_messages(self) -> Iterator[Message]:
        """Return an iterator of messages."""

        raise NotImplementedError()


def get_client() -> Client:
    """Return an instance of a Mail Client."""

    raise NotImplementedError()
