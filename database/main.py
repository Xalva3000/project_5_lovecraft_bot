import asyncio

import queries
import sqlalchemy

import database

# database.create_tables()
# queries.SyncQuery.insert_user({'user_id':1, 'name':'Sasha'})
# queries.SyncQuery.insert_user({'user_id':2, 'name':'Alexandr'})

res = queries.SyncQuery.select_user(1)
res2 = queries.SyncQuery.select_users()

print(res)
for k, v in res.__dict__.items():
    print(k, v)
