import gtts

async def text_to_speech(text, user_id):
    tts = gtts.gTTS(
        text,
        lang="ru",
    )
    tts.save(f"tts/{user_id}-tts.mp3")


async def text_to_speech_book(text, fragment_id):
    tts = gtts.gTTS(
        text,
        lang="ru",
    )
    tts.save(f"tts/book/{fragment_id}-tts.mp3")

