from datetime import datetime

from sqlalchemy import (VARCHAR, BigInteger, ForeignKey, String, Text,
                        create_engine, text)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from database.config import settings

# асинхронное подключение
async_engine = create_async_engine(url=settings.load_driver_url(), echo=True)
# синхронное подключение
sync_engine = create_engine(url=settings.load_driver_url(driver="psycopg"), echo=True)
# асинхронная сессия
async_session = async_sessionmaker(async_engine)
# синхронная сессия
sync_session = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass


class UsersOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    current_dict_page: Mapped[int] = mapped_column(default=0)
    current_mn_page: Mapped[int] = mapped_column(default=0)
    answers: Mapped[int] = mapped_column(default=0)
    right_answers: Mapped[int] = mapped_column(default=0)
    wrong_answers: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

    def __str__(self):
        return f"{self.__class__.__name__} {self.user_id}, {self.name}"


class UserBookmarksOrm(Base):
    __tablename__ = "userbookmarks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id"),
        nullable=False)
    page: Mapped[int] = mapped_column(nullable=False)


class UserTextOrm(Base):
    __tablename__ = "usertext"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    excerpt: Mapped[int] = mapped_column(Text, nullable=False)
    user_name: Mapped[int] = mapped_column(VARCHAR(32))
    rating: Mapped[int] = mapped_column(nullable=False, default=0)


class MinBookOrm(Base):
    __tablename__ = "min_book"

    page_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    fragment_id: Mapped[int] = mapped_column(nullable=False)
    page_text: Mapped[str] = mapped_column(nullable=False)


class MinFragments(Base):
    __tablename__ = "min_fragments"

    fragment_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    fragment: Mapped[str] = mapped_column(nullable=False)


class KabDictionary(Base):
    __tablename__ = "kabdictionary"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    term: Mapped[str] = mapped_column(String(64), nullable=False)
    translation: Mapped[str] = mapped_column(String(64), nullable=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)


class Questionable(Base):
    __tablename__ = "questionable"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object: Mapped[str] = mapped_column(Text, nullable=False)
    # note: Mapped[str] = mapped_column(Text)


def create_tables():
    async_engine.echo = False
    # Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine, checkfirst=True)
    async_engine.echo = True
