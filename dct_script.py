import asyncio

from database.queries import AsyncQuery

dct = {}
lst = []

with open("books/dct.txt", "rt", encoding="UTF-8") as file:
    content = [line.strip() for line in file.readlines()]

for row in content:
    if row and len(row) > 4:
        lst.append(row.split("\t", 1))

for k, v in lst:
    dct[k] = v


async def insert():
    await AsyncQuery.insert_kabdict_definitions(dct)


asyncio.run(insert())
