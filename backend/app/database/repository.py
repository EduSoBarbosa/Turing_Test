from sqlalchemy import func, select, update

from app.database.models import Experiment, Message


def group_counts(db):
    query = select(Experiment.experimental_group, func.count()).group_by(Experiment.experimental_group)
    return dict(db.execute(query).all())


def messages(db, experiment_id):
    query = select(Message).where(Message.experiment_id == experiment_id).order_by(Message.id)
    return list(db.scalars(query))


def update_session(db, experiment, **values):
    query = update(Experiment).where(
        Experiment.id == experiment.id,
        Experiment.status == experiment.status,
        Experiment.turns == experiment.turns,
    ).values(**values)
    return db.execute(query).rowcount == 1
