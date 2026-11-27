import csv
from io import StringIO
from statistics import mean, median

from sqlalchemy import select

from app.database.models import Evaluation, Experiment, Message
from app.schemas import Group
from app.services.prompt_service import TECHNIQUES


def metric(rows, field, aggregate=mean):
    values = [getattr(row, field) for row in rows if getattr(row, field) is not None]
    return aggregate(values) if values else None


def reply_metrics(replies):
    return {
        "mean_latency_ms": metric(replies, "latency_ms"),
        "median_latency_ms": metric(replies, "latency_ms", median),
        "mean_input_tokens": metric(replies, "input_tokens"),
        "mean_output_tokens": metric(replies, "output_tokens"),
    }


def results(db):
    groups = {}
    for group in Group:
        completed = select(Experiment.id).where(
            Experiment.experimental_group == group, Experiment.finished_at.is_not(None),
        )
        evaluations = db.scalars(select(Evaluation).where(Evaluation.experiment_id.in_(completed))).all()
        replies = db.scalars(select(Message).where(
            Message.experiment_id.in_(completed), Message.role == "assistant",
        )).all()
        valid = len(evaluations)
        human_rate = sum(e.classification == "human" for e in evaluations) / valid if valid else None
        groups[group] = {
            "technique": TECHNIQUES[group],
            "completed_experiments": len(db.scalars(completed).all()),
            "valid_evaluations": valid,
            "human_perception_rate": human_rate,
            "human_percentage": 100 * human_rate if valid else None,
            "machine_percentage": 100 * sum(e.classification == "machine" for e in evaluations) / valid if valid else None,
            "mean_confidence": metric(evaluations, "confidence"),
            "mean_naturalness": metric(evaluations, "naturalness"),
            "mean_coherence": metric(evaluations, "coherence"),
            "mean_emotional_understanding": metric(evaluations, "emotional_understanding"),
            **reply_metrics(replies),
        }

    baseline = groups[Group.BASELINE]["human_percentage"]
    differences = {}
    for group in (Group.ZERO_SHOT, Group.FEW_SHOT):
        value = groups[group]["human_percentage"]
        differences[group] = abs(value - baseline) if value is not None and baseline is not None else None
    return {"groups": groups, "absolute_difference_vs_baseline_pp": differences}


def export_csv(db):
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow([
        "experimental_group", "prompt_version", "turns", "classification", "confidence",
        "naturalness", "coherence", "emotional_understanding", "mean_latency_ms",
        "median_latency_ms", "mean_input_tokens", "mean_output_tokens",
    ])
    completed = db.execute(
        select(Experiment, Evaluation).outerjoin(Evaluation, Experiment.id == Evaluation.experiment_id)
        .where(Experiment.finished_at.is_not(None)).order_by(Experiment.experimental_group)
    )
    for experiment, evaluation in completed:
        replies = db.scalars(select(Message).where(
            Message.experiment_id == experiment.id, Message.role == "assistant",
        )).all()
        scores = [
            getattr(evaluation, field, None)
            for field in ("classification", "confidence", "naturalness", "coherence", "emotional_understanding")
        ]
        writer.writerow([
            experiment.experimental_group, experiment.prompt_version, experiment.turns,
            *scores, *reply_metrics(replies).values(),
        ])
    return output.getvalue()
