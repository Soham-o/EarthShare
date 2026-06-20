"""Repository pattern: every SQLAlchemy query for User lives here, and
nowhere else. Services depend on this interface, never on the ORM model
directly — that boundary is what makes the service layer unit-testable
without a database, and what lets the storage engine change later
without touching business logic."""
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def create(self, *, email: str, full_name: str, hashed_password: str) -> User:
        user = User(email=email.lower(), full_name=full_name, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
