LEXICON_default: dict[str, str] = {
    "greeting": ("Приветствую,",
    """Этот Бот делает доступным в telegram:
            изучаемый Вами материал,
            хранение выдержек, цитат из текстов, 
            обмен выдержками с другими участникам 
            Вашей учебной группы,
            а также спрашивает знания терминологии,
            интересующей Вас предметной области. \n    
            Получить список доступных команд: /help""",
    """Внизу ест кнопка МЕНЮ, со списком команд
    
    Основные команды 3:
        1 - читать "Молитва и Намерение"
        2 - случайный отрывок (из первоисточников)
        3 - игра "Словарь".
             
    Остальные команды вспомогательные:
        закладки, добавить отрывок, добавить термин в словарь.
             
    Кнопка "динамик" - это озвучивание текста, 
        нажми и немного подожди пока сформируется аудио файл.
             
    Если команда недоступна, нажми "отмену области команд" в меню.
    """),
    "help": """<b>Стартовая область команд:</b>
    /start - запуск бота
    /help - список команд данной области
    /my_info - прогресс в игре словарь
    /cancel - отмена, выход из области команд
    /read_book - читать сборник "Молитва и Намерение"
    /bookmarks - список Ваших закладок
    /random_excerpt - случайный отрывок на оценку
    /read_top_excerpts - читать 3 первых по рейтингу отрывка
    /add_excerpt - предложить отрывок
    /play_dict - игра "Словарь" 
    /add_term" - добавить термин в словарь
    /urls - полезные ссылки
    """,
    "unknown": """Ошибка ввода:
            команда неизвестна 
            или недоступна в данной области команд.
            \n/cancel - отмена, выход из текущей области команд""",
    "cancel-denied": "Пока нечего отменять",
    "Cancel": "Возврат к начальной области команд",
    "urls": """Полезные ссылки:
            Прямая аудио трансляция ББ, русская
            https://icecast.kab.tv/live1-rus-574bcfd5.mp3
            Прямая аудио трансляция ББ, english
            http://icecast.kab.tv/live1-eng-574bcfd5.mp3
            Словарь из игры:
            http://www.kabbalah.info/rus/content/view/full/59550
            """,
    "my_info": ('Ваш прогресс:', 'Всего ответов:', 'Правильные ответы:', 'Неверные ответы:')
}


LEXICON_dict: dict[str, str] = {
    "add_term": "Введите\n"
            "\tтермин, перевод и объяснение,"
            "\nразделяя их двумя заками $."
            "\n\n<b>Пример:</b>"
            "\n{термин}$${перевод}$${о б ъ я с н е н и е}"
            "\n\nили без перевода:"
            "\n{термин}$$$${о б ъ я с н е н и е}"
            "\n\n/cancel - отмена ввода",
    "cancel": 'Отмена области команд: Игра "Словарь"',
    "user_right_answer": "Верно",
    "user_wrong_answer": "Неверно",
    "system_right_answer": ("Верный ответ:",
                            "Перевод:",
                            "Определение:"),
    "add_cancel": """Ввод нового определения отменен.\n
            Возврат к начальной области команд.
            /help""",
    "add_success": "Новый термин добавлен в словарь.",
    "report": "Определение отправлено на проверку.",
    "help": """<b>Область команд: Игра "Словарь":</b>
            /cancel - выйти из игры
            /play_dict - начать игру
            /add_term - добавить термин
            /reset_stats - сброс игровой статистики""",
    "reset_stats": "Игровая статистика сброшена",
    "need_more_terms": """В базе данных недостаточно терминов
            для составления тестов.
            \n/add_term - добавить термин"""
}

LEXICON_reading_book: dict[str, str] = {
    "cancel": 'отмена области команд чтения "Молитвы и намерения"',
    "help": '''<b>Область команд чтения книги:</b>
    /read_book - читать сборник "Молитва и Намерение"
    /стр ### - открыть страницу сборник "Молитва и Намерение"
    /cancel - отмена чтения подборки
    /bookmarks - Ваши закладки
    '''
}


LEXICON_bookmarks: dict[str, str] = {
    "/bookmarks": "<b>Это список ваших закладок:</b>",
    "edit_bookmarks": "<b>Редактировать закладки</b>",
    "edit_bookmarks_button": "❌ РЕДАКТИРОВАТЬ",
    "add_bookmark": "Страница добавлена в закладки!",
    "bookmark_limit": "Достигнут предел.",
    "del": "❌",
    "cancel": "ОТМЕНИТЬ",
    "cancel_text": "/continue - продолжить чтение",
    "no_bookmarks": """У вас пока нет ни одной закладки.\n
        Чтобы добавить страницу в закладки - во время чтения 
        книги нажмите на кнопку с номером этой страницы\n
        /continue - продолжить чтение"""
}

LEXICON_excerpts: dict[str: str] = {
    "exit_excerpts": "Отмена области команд работы с отрывками",
    "cancel_adding_excerpt": "Ввод отменен",
    "added_by": "...добавил:",
    "no_excerpts": """Список отрывков пуст. 
                Добавьте отрывок командой /add_excerpt""",
    "add_excerpt": """Введите целиком отрывок, которым хотите поделиться.\n
                /cancel - отмена ввода""",
    "adding_error": "Ошибка при добавлении отрывка",
    "adding_success": "Отрывок добавлен",
    "report_excerpt": "Отрывок отправлен на проверку",
    "only_one_excerpt": "В базе данных только один отрывок",
    "mark_accepted": "Оценка единственного отрывка принята"
}


LEXICON_COMMANDS: dict[str, str] = {
    "/start": "запуск бота",
    "/help": "список команд",
    "/read_book": 'читать "Молитва и Намерение"',
    "/bookmarks": "закладки",
    "/random_excerpt": "случайный отрывок",
    "/add_excerpt": "предложить отрывок",
    "/read_top_excerpts": "читать 3 популярных отрывка",
    "/play_dict": 'игра "Словарь"',
    "/add_term": "добавить термин в словарь",
    "/my_info": "прогресс в игре словарь",
    "/urls": "полезные ссылки",
    "/cancel": "отмена, выход из области команд"
}
