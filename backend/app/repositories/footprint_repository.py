from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.footprint import ActionCompletion, FootprintRecord


class FootprintRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> FootprintRecord:
        record = FootprintRecord(**kwargs)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def latest(self, user_id: str) -> FootprintRecord | None:
        return (
            self.db.query(FootprintRecord)
            .filter(FootprintRecord.user_id == user_id)
            .order_by(desc(FootprintRecord.created_at))
            .first()
        )

    def history(self, user_id: str, limit: int = 12) -> list[FootprintRecord]:
        return (
            self.db.query(FootprintRecord)
            .filter(FootprintRecord.user_id == user_id)
            .order_by(desc(FootprintRecord.created_at))
            .limit(limit)
            .all()[::-1]
        )


class ActionCompletionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: str) -> list[ActionCompletion]:
        return self.db.query(ActionCompletion).filter(ActionCompletion.user_id == user_id).all()

    def get(self, user_id: str, action_id: str) -> ActionCompletion | None:
        return (
            self.db.query(ActionCompletion)
            .filter(ActionCompletion.user_id == user_id, ActionCompletion.action_id == action_id)
            .first()
        )

    def create(self, *, user_id: str, action_id: str, kg_co2_saved: float) -> ActionCompletion:
        completion = ActionCompletion(user_id=user_id, action_id=action_id, kg_co2_saved=kg_co2_saved)
        self.db.add(completion)
        self.db.commit()
        self.db.refresh(completion)
        return completion
