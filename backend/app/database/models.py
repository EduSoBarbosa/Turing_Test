from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now():
    # SQLite stores naive timestamps. Values in the database are UTC.
    return datetime.now(UTC).replace(tzinfo=None)


class Base(DeclarativeBase):
    pass


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id: Mapped[str] = mapped_column(primary_key=True)
    technique: Mapped[str]
    version: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(primary_key=True)
    experimental_group: Mapped[str] = mapped_column(index=True)
    model_name: Mapped[str]
    prompt_version: Mapped[str | None] = mapped_column(ForeignKey("prompt_versions.id"))
    status: Mapped[str]
    max_messages: Mapped[int]
    max_message_length: Mapped[int]
    temperature: Mapped[float]
    top_p: Mapped[float]
    max_output_tokens: Mapped[int]
    turns: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    finished_at: Mapped[datetime | None]


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[str] = mapped_column(ForeignKey("experiments.id"), index=True)
    role: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    latency_ms: Mapped[float | None]
    input_tokens: Mapped[int | None]
    output_tokens: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[str] = mapped_column(ForeignKey("experiments.id"), unique=True)
    classification: Mapped[str]
    confidence: Mapped[int]
    naturalness: Mapped[int]
    coherence: Mapped[int]
    emotional_understanding: Mapped[int]
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
