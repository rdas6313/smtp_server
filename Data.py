from dataclasses import dataclass
from typing import List


@dataclass
class Message:
    sender: str
    recipients: List[str]
    message: str

    def clear(self):
        self.sender = None
        self.recipients = []
        self.message = None


@dataclass
class Request:
    message: str
