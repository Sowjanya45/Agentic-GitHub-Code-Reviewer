"""ORM models. code_chunks (pgvector) is added in Phase 6."""
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    github_account: Mapped["GitHubAccount | None"] = relationship(back_populates="user", uselist=False)
    repositories: Mapped[list["Repository"]] = relationship(back_populates="user")


class GitHubAccount(Base):
    __tablename__ = "github_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    github_user_id: Mapped[int] = mapped_column(Integer, unique=True)
    # Stored server-side only; encrypted at rest from Phase 2. Never sent to the frontend.
    access_token_encrypted: Mapped[str | None] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="github_account")


class Repository(Base):
    __tablename__ = "repositories"
    __table_args__ = (UniqueConstraint("user_id", "github_repo_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    github_repo_id: Mapped[int] = mapped_column(Integer)
    full_name: Mapped[str] = mapped_column(String(255))
    default_branch: Mapped[str | None] = mapped_column(String(255))

    user: Mapped[User] = relationship(back_populates="repositories")
    pull_requests: Mapped[list["PullRequest"]] = relationship(back_populates="repository")


class PullRequest(Base):
    __tablename__ = "pull_requests"
    __table_args__ = (UniqueConstraint("repository_id", "number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(500))
    author: Mapped[str | None] = mapped_column(String(255))
    head_sha: Mapped[str | None] = mapped_column(String(64))

    repository: Mapped[Repository] = relationship(back_populates="pull_requests")
    reviews: Mapped[list["Review"]] = relationship(back_populates="pull_request")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    pull_request_id: Mapped[int] = mapped_column(ForeignKey("pull_requests.id", ondelete="CASCADE"))
    # QUEUED | FETCHING | ANALYZING | REVIEWING | VALIDATING | COMPLETED | FAILED
    status: Mapped[str] = mapped_column(String(20), default="QUEUED")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)

    pull_request: Mapped[PullRequest] = relationship(back_populates="reviews")
    findings: Mapped[list["Finding"]] = relationship(back_populates="review", cascade="all, delete-orphan")


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id", ondelete="CASCADE"))
    agent: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(20))  # BUG | SECURITY | QUALITY
    severity: Mapped[str] = mapped_column(String(20))  # LOW | MEDIUM | HIGH | CRITICAL
    confidence: Mapped[float] = mapped_column(Float)
    file: Mapped[str] = mapped_column(String(1000))
    line_start: Mapped[int] = mapped_column(Integer)
    line_end: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(500))
    problem: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list[str]] = mapped_column(JSONB, default=list)
    recommendation: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="VALID")  # VALID | INVALID | UNCERTAIN

    review: Mapped[Review] = relationship(back_populates="findings")
