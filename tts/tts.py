import gtts


def text_to_speech(text, user_id):
    tts = gtts.gTTS(
        text,
        lang="ru",
    )
    tts.save(f"tts/{user_id}-tts.mp3")
