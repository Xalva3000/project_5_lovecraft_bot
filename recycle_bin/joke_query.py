from sqlalchemy import select, update

from database.database import async_session, Joke, UsersOrm


async def select_all_joke_ids():
	"""SELECT id
	FROM Joke"""
	async with async_session() as session:
		stmt = select(Joke.id)
		result = await session.execute(stmt)
		return result.scalars().all()


async def select_joke(joke_id):
	"""SELECT *
	FROM joke
	WHERE id = {joke_id};"""
	async with async_session() as session:
		result = await session.get(Joke, joke_id)
		return result


async def insert_user_joke(text, name):
	"""INSERT INTO joke (joke, user_name)
	VALUES ({text}, {name});"""
	async with async_session() as session:
		session.add(Joke(joke=text, user_name=name))
		await session.commit()


async def update_joke(joke_id, joke):
	"""update joke
	set joke = '{text}'
	where id = {joke_id};"""
	async with async_session() as session:
		stmt = update(Joke).where(Joke.id == joke_id).values(joke=joke)
		await session.execute(stmt)
		await session.commit()


async def update_user_current_joke(user_id, new_joke_id):
	async with async_session() as session:
		stmt = update(UsersOrm).where(UsersOrm.user_id == user_id).values(current_joke=new_joke_id)
		await session.execute(stmt)
		await session.commit()


async def select_user_current_joke(user_id):
	"""select current_joke
	from users
	where user_id = {user_id};"""
	async with async_session() as session:
		user = await session.get(UsersOrm, user_id)
		return user.current_joke
