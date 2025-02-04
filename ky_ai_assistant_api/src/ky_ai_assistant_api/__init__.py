from typing import Protocol


class Thread(Protocol):
    """A conversation thread."""

    def post(self, message: str) -> str:
        """Post a message to the thread.

        The method returns the response of the AI Assistant.
        """
        raise NotImplementedError()


class Client(Protocol):
    """An AI Assistant Client used to maintain conversation threads."""

    def new_thread(self, message: str) -> Thread:
        """Create a new thread."""
        raise NotImplementedError()


def get_client() -> Client:
    """Return an instance of a AI Assistant Client."""
    raise NotImplementedError()
