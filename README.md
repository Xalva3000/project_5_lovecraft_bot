Telegram bot. lovecraft_bot

Работает 6 месяцев.

Суть проекта: 
Чтение или озвучивание книги постранично, 
хранение отрывков, заметок, закладок, новых слов с определениями и переводом.
+ игра викторина с определениями новы слов.

Проект обновлялся множество раз, больше 30. 
Некоторые архитектурные решения не выдерживают критики,
но это то, что мне нужно в учебном проекте.
Я хочу чувствовать какие трудности это создает.

Подробное описание.
Возможность читать книгу постранично, 
Попросить бота прислать аудио озвученной страницы или фрагмента, чтобы слушать, пока нет возможности читать с экрана.
Возможность делать закладки в книге.
Возможность сохранять отрывки, выписки, и также просить бота зачитать их.
Возможность записывать свои текста, и просить бота зачитать их.

Игра «Словарь»: записываете новые для себя слова, с определением и переводом. После чего появляется возможность играть в викторину на подобии ТВ передачи «Кто хочет стать миллионером». Выводится определение термина, и 4 варианта ответа сложенных из других внесенных слов (неверные ответы выбираются случайным образом из списка всех терминов). И нужно угадать слово по определению. За верный ответ начисляются очки, которые видно в главном меню.
Можно использовать для изучения английской литературы и английского языка и слов, либо для технической литературы и технических терминов.

Использованные технологии: Ubuntu, Git, GitHub, Python, PostgreSQL, Aiogram, SQLAlchemy, Alembic, GoogleTTS, 
Redis для антиспам middleware, Регулярные выражения, Запросы исполняются асинхронно, кроме озвучивания текста, 
сервер опрашивается технологией long polling. 
Не применял WebHook, чтобы избежать бана со стороны Telegram в случае недоступности сервера 
и не привлекать внимание DDOS-еров.
