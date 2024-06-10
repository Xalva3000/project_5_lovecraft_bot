from random import choice
from typing import Iterable, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.sql.expression import func

from database.database import (Book, UserBookmarks, Letter, Dictionary, Questionable, UsersOrm, UserTextOrm,
                               async_session)
from database.temporary_info import usersdictplaycache

"""Файл для хранения асинхронных запросов"""


class AsyncQuery:
    @staticmethod
    async def insert_user(u_id: int, name: str):
        """INSERT INTO users (user_id, name)
        VALUES ({u_id},{name});"""
        async with async_session() as session:
            if isinstance(u_id, int) and isinstance(name, str | None):
                session.add(UsersOrm(user_id=u_id, name=name))
                await session.commit()
            else:
                return "wrong data types"

    @staticmethod
    async def select_user(u_id: int) -> Optional[UsersOrm]:
        """SELECT *
        FROM users
        WHERE user_id = {u_id};"""
        async with async_session() as session:
            result = await session.get(UsersOrm, u_id)
            return result

    @staticmethod
    async def select_user_book_page(u_id: int):
        """SELECT current_mn_page
        FROM users
        WHERE user_id = {u_id};"""
        async with async_session() as session:
            result = await session.get(UsersOrm, u_id)
            return result.current_book_page

    @staticmethod
    async def update_users_book_page(u_id: int, new_page: str | int = "forward"):
        """UPDATE users
        SET current_mn_page = {new_page or +- 1}
        WHERE user_id = {u_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, u_id)
            if new_page == "forward":
                user.current_book_page += 1
            elif new_page == "backward" and user.current_book_page > 1:
                user.current_book_page -= 1
            elif isinstance(new_page, int) and new_page >= 1:
                user.current_book_page = new_page
            await session.commit()

    @staticmethod
    async def select_user_answers(u_id):
        """SELECT answers
        FROM users
        WHERE user_id = {u_id}"""
        async with async_session() as session:
            user = await session.get(UsersOrm, u_id)
            return user.answers

    @staticmethod
    async def update_users_wrong_answer(u_id):
        """UPDATE users
        SET answers = answers + 1,
        wrong_answers = wrong_answers + 1
        where user_id = {u_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, u_id)
            user.answers += 1
            user.wrong_answers += 1
            await session.commit()

    @staticmethod
    async def update_users_right_answer(u_id):
        """UPDATE users
        SET answers = answers + 1,
        right_answers = right_answers + 1
        where user_id = {u_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, u_id)
            user.answers += 1
            user.right_answers += 1
            await session.commit()

    @staticmethod
    async def reset_users_stats(u_id):
        """UPDATE users
        SET answers = 0,
        right_answers = 0,
        wrong_answers = 0
        where user_id = {u_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, u_id)
            user.answers = 0
            user.right_answers = 0
            user.wrong_answers = 0
            await session.commit()

    @staticmethod
    async def insert_book_pages(book: dict[int:tuple]):
        """INSERT INTO min_book (page_id, page_text)
        VALUES ({key}, {page_text});"""
        async with async_session() as session:
            for key, page_text in book.items():
                session.add(
                    Book(page_id=key, page_text=page_text)
                )
            await session.commit()

    @staticmethod
    async def select_book_page(page: int | Iterable):
        """SELECT page_text, fragment_id
        FROM min_book
        WHERE page_id {= page or in set(pages)};"""
        async with async_session() as session:
            if isinstance(page, int):
                result = await session.get(Book, page)
                if result:
                    return result.page_text
                else:
                    return None
            else:
                stmt = (
                    select(Book)
                    .where(Book.page_id.in_(set(page)))
                    .limit(15)
                )
                result = await session.execute(stmt)
                return result.scalars().fetchall()


    # запрос максимального номера страницы для клавиатуры пагинации книги
    @staticmethod
    async def select_max_book_page() -> int:
        """SELECT max(page_id)
        FROM min_book;"""
        async with async_session() as session:
            stmt = select(func.max(Book.page_id))
            result = await session.execute(stmt)
            return result.scalars().one()

    @staticmethod
    async def insert_bookmark(user_id, page):
        """INSERT INTO userbookmarks(user_id, page)
        VALUES ({user_id}, {page});"""
        async with async_session() as session:
            session.add(UserBookmarks(user_id=user_id, page=page))
            await session.commit()


    @staticmethod
    async def select_users_bookmarks(user_id):
        """SELECT page
        FROM userbookmarks
        WHERE user_id = {user_id};"""
        async with async_session() as session:
            stmt = select(UserBookmarks.page).filter_by(user_id=user_id)
            result = await session.execute(stmt)
            return result.scalars().fetchall()

    @staticmethod
    async def delete_users_bookmark(user_id, page):
        """DELETE
        FROM userbookmarks
        WHERE user_id = {user_id} AND page = {page};"""
        async with async_session() as session:
            stmt = delete(UserBookmarks).filter_by(user_id=user_id, page=page)
            await session.execute(stmt)
            await session.commit()

    # @staticmethod
    # async def insert_book_fragments(book: dict[int:tuple]):
    #     """INSERT INTO min_fragments (fragment_id, fragment)
    #     VALUES ({key}, {value});"""
    #     async with async_session() as session:
    #         for key, value in book.items():
    #             session.add(MinFragments(fragment_id=key, fragment=value))
    #         await session.commit()

    # @staticmethod
    # async def select_book_fragment(fragment_num):
    #     """SELECT *
    #     FROM min_fragments
    #     WHERE fragment_id = fragment_num;"""
    #     async with async_session() as session:
    #         result = await session.get(MinFragments, fragment_num)
    #         return result.fragment
    #
    # @staticmethod
    # async def select_fragment_id(page_id):
    #     """SELECT fragment_id
    #     FROM min_book
    #     WHERE page_id = {page_id};"""
    #     async with async_session() as session:
    #         result = await session.get(MinBookOrm, page_id)
    #         return result.fragment_id

    # @staticmethod
    # async def select_page_of_chapter(fragment_id):
    #     """SELECT min(page_id)
    #     FROM min_book
    #     WHERE fragment_id = {fragment_id};"""
    #     async with async_session() as session:
    #         stmt = select(func.min(MinBookOrm.page_id)).where(MinBookOrm.fragment_id == fragment_id)
    #         result = await session.execute(stmt)
    #         return result.scalar()

    # @staticmethod
    # async def select_all_fragments():
    #     """SELECT fragment
    #     FROM min_fragments
    #     ORDER BY fragment_id"""
    #     # на данный момент не используется
    #     async with async_session() as session:
    #         stmt = select(MinFragments.fragment).order_by(MinFragments.fragment_id)
    #         result = await session.execute(stmt)
    #         return result.scalars().all()

    @staticmethod
    async def select_all_excerpt_ids():
        """SELECT id
        FROM usertext"""
        async with async_session() as session:
            stmt = select(UserTextOrm.id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def delete_excerpt_by_id(excerpt_id: int):
        """DELETE FROM usertext
        WHERE excerpt_id = {excerpt_id}"""
        async with async_session() as session:
            stmt = delete(UserTextOrm).where(UserTextOrm.id == excerpt_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def select_random_excerpt(previous_num=None) -> tuple | None:
        """Возвращает случайный отрывок, за исключением предыдущего,
        если предыдущий имеется"""
        async with async_session() as session:
            random_num = previous_num

            stmt = select(UserTextOrm.id)
            lst_temp = await session.execute(stmt)
            all_excerpts = lst_temp.scalars().all()
            # если в базе ни одного отрывка или один то возвращаем None
            if (len(all_excerpts) == 0 or
                    (previous_num and len(all_excerpts) == 1)):
                return None

            # если имеется предыдущее число
            if previous_num:
                while random_num == previous_num:
                    random_num = choice(all_excerpts)
            else:
                random_num = choice(all_excerpts)
            result = await session.get(UserTextOrm, random_num)
            return result.excerpt, result.id, result.user_name


    @staticmethod
    async def select_user_current_excerpt(user_id):
        """select current_excerpt
        from users
        where user_id = {user_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, user_id)
            return user.current_excerpt


    @staticmethod
    async def update_user_current_excerpt(user_id, new_excerpt_id):
        """UPDATE users
        SET current_excerpt = {new_excerpt_id}
        where user_id = {user_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, user_id)
            user.current_excerpt = new_excerpt_id
            await session.commit()


    @staticmethod
    async def select_excerpt_by_id(excerpt_id):
        """SELECT *
        FROM user_text
        WHERE id = {excerpt_id};"""
        async with async_session() as session:
            result = await session.get(UserTextOrm, excerpt_id)
            return result

    @staticmethod
    async def insert_user_excerpt(text, name):
        """INSERT INTO usertext (excerpt, user_name)
        VALUES ({text}, {name});"""
        async with async_session() as session:
            session.add(UserTextOrm(excerpt=text, user_name=name))
            await session.commit()

    @staticmethod
    async def update_excerpt(excerpt_id, excerpt):
        """update usertext
        set excerpt = '{text}'
        where id = {excerpt_id};"""
        async with async_session() as session:
            stmt = update(UserTextOrm).where(UserTextOrm.id == excerpt_id).values(excerpt=excerpt)
            await session.execute(stmt)
            await session.commit()


    @staticmethod
    async def select_all_letter_ids():
        """SELECT id
        FROM letter"""
        async with async_session() as session:
            stmt = select(Letter.id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def select_first_letter():
        """SELECT *
        FROM letter
        WHERE id = 1;"""
        async with async_session() as session:
            letter = await session.get(Letter, 1)
            if letter:
                return letter

    @staticmethod
    async def select_letter(letter_id):
        """SELECT *
        FROM letter
        WHERE id = {letter_id};"""
        async with async_session() as session:
            result = await session.get(Letter, letter_id)
            return result


    @staticmethod
    async def insert_user_letter(text, name):
        """INSERT INTO letter (letter, user_name)
        VALUES ({text}, {name});"""
        async with async_session() as session:
            session.add(Letter(letter=text, user_name=name))
            await session.commit()

    @staticmethod
    async def update_letter(letter_id, letter):
        """update letter
        set letter = '{text}'
        where id = {letter_id};"""
        async with async_session() as session:
            stmt = update(Letter).where(Letter.id == letter_id).values(letter=letter)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_user_current_letter(user_id, new_letter_id):
        async with async_session() as session:
            stmt = update(UsersOrm).where(UsersOrm.user_id == user_id).values(current_letter=new_letter_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def select_user_current_letter(user_id):
        """select current_letter
        from users
        where user_id = {user_id};"""
        async with async_session() as session:
            user = await session.get(UsersOrm, user_id)
            return user.current_letter


    @staticmethod
    async def insert_dict_definition(dct):
        """Добавляет в словарь dict({dct}).
        INSERT INTO dictionary (term, translation, definition)
        VALUES ({term}, {translation}, {definition});"""
        async with async_session() as session:
            for term, translation, definition in dct.values():
                session.add(Dictionary(term=term,
                                          translation=translation,
                                          definition=definition
                                          ))
            await session.commit()

    @staticmethod
    async def insert_term(term_tpl):
        """Добавляет в словарь строку: термин, перевод, объяснение.
        INSERT INTO dictionary (term, translation, definition)
        VALUES ({term}, {translation}, {definition});"""
        async with async_session() as session:
            term, translation, definition = term_tpl
            session.add(Dictionary(term=term,
                                   translation=translation,
                                   definition=definition
                                   ))
            await session.commit()


    @staticmethod
    async def select_all_dict_ids():
        """SELECT id
        FROM dictionary;"""
        async with async_session() as session:
            stmt = select(Dictionary.id)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def select_excerpt(excerpt_id):
        """SELECT *
        FROM usertext
        WHERE id = {excerpt_id};"""
        async with async_session() as session:
            result = await session.get(UserTextOrm, excerpt_id)
            return result


    @staticmethod
    async def select_specific_terms(lst: list[int]):
        """SELECT *
        FROM dictionary
        WHERE id in ({lst});"""
        async with async_session() as session:
            stmt = select(Dictionary).where(Dictionary.id.in_(lst))
            result = await session.execute(stmt)
            return result.scalars().all()



    @staticmethod
    async def insert_questionable_dct(user_id):
        """INSERT INTO questionable (object)
        VALUES ({cashed_test_question[user_id]});"""
        async with async_session() as session:
            session.add(Questionable(object=str(usersdictplaycache[user_id])))
            await session.commit()

    @staticmethod
    async def insert_questionable_excerpt(report_text):
        """в таблицу сомнительных объектов вставляется строка
        кнопки REPORT, в которой указан номер отрывка
        INSERT INTO questionable (object)
        VALUES ({report_button_text_id});"""
        async with async_session() as session:
            session.add(Questionable(object=report_text))
            await session.commit()
