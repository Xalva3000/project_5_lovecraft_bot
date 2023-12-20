class IsTTSTopExcerpts(BaseFilter):
    """Фильтр сообщений от нажатия кнопки с изображением динамика,
    предназначенной для команды озвучивания популярного отрывка, выдержки.
    В сообщении также указан индекс позиции отрывка."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-top-excerpt-\d{1,3}", callback.data):
            return True
        return False



class IsNextTopExcerpt(BaseFilter):
    """Фильтр сообщений от нажатия кнопки '>>' при чтении лучших
    отрывков, с указанием индекса текущего отрывка. (0 - отрывок
    с наивысшей оценкой, 1 - второе место и тд)"""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"next_[012]", callback.data):
            return True
        return False




class IsRating(BaseFilter):
    """Фильтр сообщений от нажатия кнопки при чтении случайного отрывка
    с изображением emoji 'большой палец поднят' или 'опущен', что означает
     повышение или понижения общей оценки отрывка."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"up_\d+|down_\d+", callback.data):
            return True
        return False




@router.callback_query(IsTTSTopExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_top_excerpts(callback: CallbackQuery, bot: Bot):
    text = usertextcache[int(callback.data.replace("voice-top-excerpt-", ""))]
    await text_to_speech(text, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id,
                             audio=audio,
                             reply_markup=create_del_audio_keyboard()
                             )


@router.callback_query(IsNextTopExcerpt(), StateFilter(FSMStates.reading_excerpts))
async def process_next_top_excerpt_button(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() == FSMStates.reading_excerpts:
        pass
    else:
        await state.set_state(FSMStates.reading_excerpts)
    await load_top_excerpts()

    pos = int(callback.data.replace("next_", ""))
    if len(usertextcache) > 1:
        next_pos = (pos + 1) % len(usertextcache) if len(usertextcache) == 2 else (pos + 1) % 3
        await callback.message.edit_text(
            text=usertextcache[next_pos],
            reply_markup=create_topexcerpts_keyboard(next_pos)
        )
        await callback.answer()
    else:
        await callback.answer(text=LEXICON_excerpts["only_one_excerpt"])


@router.callback_query(IsRating(), StateFilter(FSMStates.reading_excerpts))
async def process_rating_button(callback: CallbackQuery):
    """Принимает команду на повышение или понижение (up_#) рейтинга
    определенного отрывка"""
    command = callback.data.split("_")
    await AsyncQuery.update_excerpt_rating(int(command[1]), command[0])

    tpl_text = await AsyncQuery.select_random_excerpt(int(command[1]))
    if tpl_text:
        await callback.message.edit_text(
            text=tpl_text[0] + f'\n\n{LEXICON_excerpts["added_by"]} {tpl_text[2]}',
            reply_markup=create_rating_keyboard(tpl_text[1]))
    else:
        await callback.answer(text=LEXICON_excerpts["mark_accepted"])

# @router.message(
#     Command(commands=["cancel"]), StateFilter(FSMStates.adding_excerpt)
# )
# async def process_cancel_adding_excerpt(message: Message, state: FSMContext):
#     await message.answer(text=LEXICON_excerpts["cancel_adding_excerpt"],
#                          reply_markup=create_return_menu_keyboard())
#     await state.clear()




@router.callback_query(F.data == "/read_top_excerpts")
async def process_read_excerpts_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки топ 3 по популярности отрывка"""
    await load_top_excerpts()
    if usertextcache:
        await state.set_state(FSMStates.reading_excerpts)
        await callback.message.edit_text(
            text=usertextcache[0], reply_markup=create_topexcerpts_keyboard(0)
        )
    else:
        await callback.message.edit_text(text=LEXICON_excerpts["no_excerpts"],
                                         reply_markup=create_return_menu_keyboard())


async def load_top_excerpts() -> None:
    """Загружает 3 самых популярных отрывка в кэш"""
    lst = await AsyncQuery.select_top_excerpts()
    if lst:
        for i, obj in enumerate(lst):
            usertextcache[i] = obj.excerpt


