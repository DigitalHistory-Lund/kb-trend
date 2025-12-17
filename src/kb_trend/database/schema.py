"""SQLAlchemy database schema."""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

Base = declarative_base()


class Metadata(Base):
    """System metadata table for config hash and version tracking."""

    __tablename__ = 'metadata'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Metadata(key='{self.key}', value='{self.value}')>"


class Journal(Base):
    """Newspaper/journal definitions."""

    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)

    # Relationships
    counts = relationship("Count", back_populates="journal", cascade="all, delete-orphan")
    queue_items = relationship("QueueItem", back_populates="journal", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Journal(id={self.id}, name='{self.name}')>"


class Query(Base):
    """Search queries with metadata."""

    __tablename__ = 'query'

    id = Column(Integer, primary_key=True)
    search_string = Column(String, nullable=False, index=True)
    keyword = Column(String, nullable=False, index=True)
    metadata_json = Column(JSON, nullable=True)

    # Unique constraint on search_string + keyword
    __table_args__ = (
        UniqueConstraint('search_string', 'keyword', name='uq_query_search_keyword'),
        Index('idx_query_keyword', 'keyword'),
    )

    # Relationships
    counts = relationship("Count", back_populates="query", cascade="all, delete-orphan")
    queue_items = relationship("QueueItem", back_populates="query", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Query(id={self.id}, keyword='{self.keyword}')>"


class Count(Base):
    """Hit counts from scraping."""

    __tablename__ = 'counts'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, index=True)
    query_id = Column(Integer, ForeignKey('query.id'), nullable=False)
    journal_id = Column(Integer, ForeignKey('journal.id'), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    rel = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint('year', 'query_id', 'journal_id', name='uq_count_year_query_journal'),
        Index('idx_count_query', 'query_id'),
        Index('idx_count_journal', 'journal_id'),
        Index('idx_count_year', 'year'),
    )

    # Relationships
    query = relationship("Query", back_populates="counts")
    journal = relationship("Journal", back_populates="counts")

    def __repr__(self) -> str:
        return (
            f"<Count(id={self.id}, year={self.year}, query_id={self.query_id}, "
            f"journal_id={self.journal_id}, count={self.count})>"
        )


class QueueItem(Base):
    """Scraping queue."""

    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('query.id'), nullable=False)
    journal_id = Column(Integer, ForeignKey('journal.id'), nullable=False)
    year = Column(String, nullable=False)  # Can be "all" or specific year
    status = Column(String, default='pending', index=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('query_id', 'journal_id', 'year', name='uq_queue_query_journal_year'),
        Index('idx_queue_status', 'status'),
        Index('idx_queue_query', 'query_id'),
    )

    # Relationships
    query = relationship("Query", back_populates="queue_items")
    journal = relationship("Journal", back_populates="queue_items")

    def __repr__(self) -> str:
        return (
            f"<QueueItem(id={self.id}, query_id={self.query_id}, "
            f"journal_id={self.journal_id}, status='{self.status}')>"
        )
