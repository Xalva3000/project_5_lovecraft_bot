import asyncio
from pprint import pprint

from database.queries import AsyncQuery


def _get_part_text(text, start, page_size):
    char_end= ',.!:;?'
    part = text[start:start+page_size]
    for i_b in range(-1,-len(part)-1, -1):
        if part[i_b] in char_end:
            end = (start + page_size + i_b + 1) if (start + page_size + i_b + 1) <= len(text) else len(text)
            result = text[start:end]
            if result[-1] in char_end and result[-2] in char_end and result[-3] not in char_end:
                result = _get_part_text(text, start, page_size-2)[0]
            return result, len(result)


book: dict[int, str] = {}
PAGE_SIZE = 1050
book_path = "books/lovecraft_book.txt"

# Дополните эту функцию, согласно условию задачи
def prepare_book(path: str) -> None:
    indent = 0
    count = 1
    with open(path, 'rt', encoding='UTF-8') as file_in:
        content = file_in.read()
    while indent < len(content):
        tpl = _get_part_text(content, indent, PAGE_SIZE)
        if tpl[0]:
            book[count] = tpl[0].lstrip()
            indent += tpl[1]
            count += 1
        else:
            break

async def paging():
    prepare_book(book_path)
    await AsyncQuery.insert_book_pages(book)
    # pprint(book)



if __name__ == "__main__":
    asyncio.run(paging())
