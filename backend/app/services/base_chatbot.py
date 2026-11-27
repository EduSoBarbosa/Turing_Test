from dataclasses import dataclass
from typing import Protocol

from app.database.models import Experiment, Message


@dataclass(frozen=True)
class Reply:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None


class ChatbotError(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


class Chatbot(Protocol):
    def reply(self, experiment: Experiment, history: list[Message], prompt: str | None) -> Reply: ...
