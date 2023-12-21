from itertools import cycle


def next_unordered_number(lst: list[int], current_number: int, backward=False):
    """В неупорядоченной последовательности находит следующее число
    (по умолчанию в стороне увеличения чисел).
    Можно указать, что следующее число нужно искать
    в сторону уменьшения чисел."""

    if not lst:
        return

    if current_number not in lst or len(lst) == 1:
        return lst[0]

    cycled_lst = cycle(sorted(lst, reverse=backward))

    for _ in range(len(lst)+1):
        if next(cycled_lst) == current_number:
            return next(cycled_lst)
    return lst[0]
