from typing import List, Optional

"""models for api"""

class Header:
    """Represents an email header."""
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class Email:
    """Represents an email message."""
    def __init__(self, email_id: str, sender: str, subject: str, snippet: Optional[str] = None, headers: Optional[List[Header]] = None):
        self.email_id = email_id
        self.sender = sender
        self.subject = subject
        self.snippet = snippet
        self.headers = headers or []

    def __repr__(self):
        return f"Email(id={self.email_id}, sender={self.sender}, subject={self.subject}, snippet={self.snippet})"
