from database.queries import AsyncQuery
from database.temporary_info import usersdictplaycache
from random import sample, randint


async def load_answers(user_id: int) -> str:
    """Загружаем вопрос и варианты ответов в кэш,
    возвращает вопрос(текст объяснения верного термина)"""
    if user_id in usersdictplaycache:
        del usersdictplaycache[user_id]
    all_ids = await AsyncQuery.select_all_dict_ids()
    if len(all_ids) < 4:
        return None
    objects = await AsyncQuery.select_specific_terms(sample(all_ids, 4))

    random_num = randint(0, 3)
    usersdictplaycache[user_id] = {
        "current_data": (objects[random_num].term,
                         objects[random_num].translation,
                         objects[random_num].definition)
    }
    for i, obj in enumerate(objects):
        if i == random_num:
            usersdictplaycache[user_id][i] = (obj.term, "right")
        else:
            usersdictplaycache[user_id][i] = (obj.term, "wrong")
    return objects[random_num].definition
