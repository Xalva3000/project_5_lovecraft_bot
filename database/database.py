from datetime import datetime

from sqlalchemy import (VARCHAR, BigInteger, ForeignKey, String, Text,
                        create_engine, text, Integer)
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
    current_book_page: Mapped[int] = mapped_column(default=1, server_default='1')
    # current_psalter_page: Mapped[int] = mapped_column(default=0)
    # current_joke: Mapped[int] = mapped_column(default=0)
    current_excerpt: Mapped[int] = mapped_column(Integer, default=1, server_default='1')
    current_letter: Mapped[int] = mapped_column(Integer, default=1, server_default='1')
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


class Book(Base):
    __tablename__ = "book"

    page_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    # fragment_id: Mapped[int] = mapped_column(nullable=False)
    page_text: Mapped[str] = mapped_column(nullable=False)


class UserBookmarks(Base):
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
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[str] = mapped_column(VARCHAR(32))
    rating: Mapped[int] = mapped_column(nullable=False, default=0)


class Letter(Base):
    __tablename__ = "letter"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    letter: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[str] = mapped_column(VARCHAR(32))


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    term: Mapped[str] = mapped_column(String(64), nullable=False)
    translation: Mapped[str] = mapped_column(String(64), nullable=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)


class Questionable(Base):
    __tablename__ = "questionable"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object: Mapped[str] = mapped_column(Text, nullable=False)


def create_tables():
    async_engine.echo = False
    # Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine, checkfirst=True)
    async_engine.echo = True

#
# class NewWordsDictionary(Base):
#     __tablename__ = "new_words_dictionary"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     term: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
#     translation: Mapped[str] = mapped_column(String(64), nullable=True)
#     definition: Mapped[str] = mapped_column(Text, nullable=False)


# class MinFragments(Base):
#     __tablename__ = "min_fragments"
#
#     fragment_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     fragment: Mapped[str] = mapped_column(nullable=False)
#
# class EnglishBook(Base):
#     __tablename__ = "eng_book"
#
#     page_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     page_text: Mapped[str] = mapped_column(nullable=False)

#
# class Joke(Base):
#     __tablename__ = 'joke'
#
#     id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
#     joke: Mapped[str] = mapped_column(Text, nullable=False)
#     user_name: Mapped[str] = mapped_column(VARCHAR(32))


# class PsalterPages(Base):
#     __tablename__ = 'psalter_pages'
#
#     page_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
#     psalm_id: Mapped[int] = mapped_column(nullable=False)
#     psalm_text: Mapped[str] = mapped_column(Text, nullable=False)
#
#
# class PsalterPsalms(Base):
#     __tablename__ = "psalter_psalms"
#
#     psalm_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
#     psalm_text: Mapped[str] = mapped_column(nullable=False)



