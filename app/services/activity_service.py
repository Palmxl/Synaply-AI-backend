from sqlalchemy.orm import Session

from app.models.activity_log import (
    ActivityLog
)


def log_activity(
    db: Session,
    owner_id: int,
    action: str,
    description: str
):
    activity = ActivityLog(
        owner_id=owner_id,
        action=action,
        description=description
    )

    db.add(activity)

    db.commit()