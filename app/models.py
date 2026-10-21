from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import DatabaseBase

note_tags = Table(
    "note_tags",
    DatabaseBase.metadata,
    Column("note_id", Integer, ForeignKey("notes.note_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True),
)


class User(DatabaseBase):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Notes(DatabaseBase):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True)
    pinned = Column(Boolean, default=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    archived = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")
    checklist_items = relationship(
        "ChecklistItem", back_populates="note", cascade="all, delete-orphan"
    )


class Tag(DatabaseBase):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_tag_name"),)

    tag_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    name = Column(String(40), nullable=False)
    notes = relationship("Notes", secondary=note_tags, back_populates="tags")


class ChecklistItem(DatabaseBase):
    __tablename__ = "checklist_items"

    item_id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.note_id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(String(300), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    position = Column(Integer, default=0, nullable=False)
    note = relationship("Notes", back_populates="checklist_items")
