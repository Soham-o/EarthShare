"""Auth business logic: sits between the API layer and the repository.
Routes never touch bcrypt, JWT, or the User model directly — they call
this service, which is what makes auth logic unit-testable without
spinning up FastAPI at all (see tests/test_auth.py)."""
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister


class AuthError(Exception):
    """Raised for any auth failure the API layer should turn into 401/409."""


class EmailAlreadyRegistered(AuthError):
    pass


class InvalidCredentials(AuthError):
    pass


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, payload: UserRegister) -> tuple[User, str]:
        if self.repo.get_by_email(payload.email):
            raise EmailAlreadyRegistered("An account with this email already exists.")
        user = self.repo.create(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        token = create_access_token(subject=user.id)
        return user, token

    def login(self, payload: UserLogin) -> tuple[User, str]:
        user = self.repo.get_by_email(payload.email)
        # Constant-shape work whether or not the user exists, to avoid
        # leaking account existence via timing.
        valid = verify_password(payload.password, user.hashed_password) if user else False
        if not user or not valid:
            raise InvalidCredentials("Incorrect email or password.")
        token = create_access_token(subject=user.id)
        return user, token
