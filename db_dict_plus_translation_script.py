import asyncio
from pprint import pprint

from database.queries import AsyncQuery

dct = {}
lst = []

with open("books/dct_plus_translation.txt", "rt", encoding="UTF-8") as file:
    content = [line.strip() for line in file.readlines()]

print(len(content))
for row in content:
    if row:
        lst.append(row.split("\t", 2))

print(len(lst))

for k, t, v in lst:
    if k in dct:
        print(k, t, v)
    dct[k] = (k, t, v)


print(len(dct))

async def insert():
    await AsyncQuery.insert_kabdict_definition(dct)


asyncio.run(insert())

