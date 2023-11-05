import asyncio
import re

from database.queries import AsyncQuery

# from pprint import pprint


# добавляет спец символ в конкретный файл и по нему разделяет текст на главы
def fragmentation(path) -> list[str]:
    with open(path, "rt", encoding="UTF-8") as file_in:
        content = file_in.read()
    regex = r"Фрагмент"
    add_spec_symbol = re.sub(regex, "$$ Фрагмент", content)
    regex_split = r"\$\$ "
    new_content = re.split(regex_split, add_spec_symbol)
    return new_content


# путь и имя для нового файла
def rename_path(path):
    lst = path.rsplit("\\", 1)
    filename = lst[-1].split(".")
    filename[0] = filename[0] + "-fragmented"
    lst[-1] = ".".join(filename)
    return "\\".join(lst)


# отмеряет длину страницы
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    char_end = ",.!:;?"
    part = text[start: start + page_size]
    for i_b in range(-1, -len(part) - 1, -1):
        if part[i_b] in char_end:
            end = (
                (start + page_size + i_b + 1)
                if (start + page_size + i_b + 1) <= len(text)
                else len(text)
            )
            result = text[start:end]
            if (
                result[-1] in char_end
                and result[-2] in char_end
                and result[-3] not in char_end
            ):
                result = _get_part_text(text, start, page_size - 2)[0]
            return result, len(result)


# Функция, формирующая словарь книги
def prepare_fragmented_book(fragmented_book: list, dct: dict, page_size):
    indent = 0
    count = 0
    chapter = 0
    for fragment in fragmented_book:
        if len(fragment) < page_size:
            dct[count] = (chapter, fragment)
            count += 1
            chapter += 1
        else:
            while indent < len(fragment):
                tpl = _get_part_text(fragment, indent, page_size)
                if tpl[0]:
                    dct[count] = (chapter, tpl[0].lstrip())
                    indent += tpl[1]
                    count += 1
                else:
                    break
            chapter += 1
            indent = 0


PAGE_SIZE = 1050
book = {}
book_path = "books\\MIN.txt"
book_name = ""


async def paging():
    fragmented_book: list[str] = fragmentation(book_path)
    dct_fragmented_book = {i: text for i, text in enumerate(fragmented_book)}
    await AsyncQuery.insert_book_fragments(dct_fragmented_book)

    prepare_fragmented_book(fragmented_book, book, PAGE_SIZE)
    await AsyncQuery.insert_book_pages(book)
    await AsyncQuery.select_book_fragment(3)


if __name__ == "__main__":
    asyncio.run(paging())
