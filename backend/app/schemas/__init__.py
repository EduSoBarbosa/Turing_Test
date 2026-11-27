from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Group(StrEnum):
    ELIZA = "A"
    BASELINE = "B"
    ZERO_SHOT = "C"
    FEW_SHOT = "D"


class Status(StrEnum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    AWAITING_EVALUATION = "AWAITING_EVALUATION"
    EVALUATED = "EVALUATED"
    REVEALED = "REVEALED"


class Payload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class Start(Payload):
    acknowledged: bool


class MessageInput(Payload):
    content: str = Field(min_length=1)


class EvaluationInput(Payload):
    classification: Literal["human", "machine"]
    confidence: int = Field(ge=0, le=100)
    naturalness: int = Field(ge=1, le=5)
    coherence: int = Field(ge=1, le=5)
    emotional_understanding: int = Field(ge=1, le=5)
    comment: str | None = Field(None, max_length=2000)


class SessionView(BaseModel):
    id: UUID
    status: Status
    remaining_messages: int
    max_messages: int
    max_message_length: int
    notice: str


class MessageView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: Literal["user", "assistant"]
    content: str
    created_at: datetime


class TurnView(BaseModel):
    session: SessionView
    messages: list[MessageView]


class RevealView(BaseModel):
    session: SessionView
    experimental_group: Group
    model_name: str
    provider: str
    technique: str
    prompt_version: str | None


class PromptView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    technique: str
    version: str
    content: str
    content_hash: str
    created_at: datetime
