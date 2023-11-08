import asyncio
from pprint import pprint

from database.queries import AsyncQuery

dct = {}
lst = []

with open("books/dct_plus_translation.txt", "rt", encoding="UTF-8") as file:
    content = [line.strip() for line in file.readlines()]


for row in content:
    if row and len(row) > 4:
        lst.append(row.split("\t", 2))

for k, t, v in lst:
    dct[k] = (k, t, v)


async def insert():
    await AsyncQuery.insert_kabdict_definition(dct)


asyncio.run(insert())

