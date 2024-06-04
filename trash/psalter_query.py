from sqlalchemy import select, update, func
from database.database import async_session, UsersOrm
from database.database import PsalterPages, PsalterPsalms


def insert_psalter_fragments(psalms: dict[int:tuple]):
	"""INSERT INTO psalter_psalms (psalm_id, psalm)
	VALUES ({key}, {value});"""
	with async_session() as session:
		for key, value in psalms.items():
			session.add(PsalterPsalms(psalm_id=key, psalm_text=value))
		session.commit()


def insert_psalter_pages(psalter: dict[int:tuple]):
	"""INSERT INTO psalter_pages (page_id, fragment_id, page_text)
	VALUES ({key}, {tpl[0]}, {tpl[1]});"""
	with async_session() as session:
		for key, tpl in psalter.items():
			session.add(
				PsalterPages(page_id=key, psalm_id=tpl[0], psalm_text=tpl[1])
			)
		session.commit()


async def get_max_psalter_page():
	"""SELECT MAX(page_id)
	from psalter_pages"""
	async with async_session() as session:
		stmt = select(func.max(PsalterPages.page_id))
		result = await session.execute(stmt)
		return result.scalars().one()


async def get_psalter_page_by_page_id(page_id: int):
	"""SELECT psalm_text
	from psalter_pages
	WHERE page_id = {page_id}"""
	async with async_session() as session:
		page = await session.get(PsalterPages, page_id)
		return page.psalm_text


async def get_psalm_by_psalm_id(psalm_id: int):
	"""SELECT psalm_text
		from psalter_pages
		WHERE page_id = {page_id}"""
	async with async_session() as session:
		psalm = await session.get(PsalterPsalms, psalm_id)
		return psalm.psalm_text


async def update_users_psalter_page(u_id: int, new_page: str | int = "forward"):
	"""UPDATE users
	SET current_psalter_page = {new_page or +- 1}
	WHERE user_id = {u_id};"""
	async with async_session() as session:
		user = await session.get(UsersOrm, u_id)
		if new_page == "forward":
			user.current_psalter_page += 1
		elif new_page == "backward" and user.current_psalter_page > 0:
			user.current_psalter_page -= 1
		elif isinstance(new_page, int) and new_page >= 0:
			user.current_psalter_page = new_page
		await session.commit()


# получить данные юзера = AsyncQuery.select_user(u_id)