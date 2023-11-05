import gtts


def text_to_speech(text, id):
    tts = gtts.gTTS(
        text,
        lang="ru",
    )
    tts.save(f"tts/{id}-tts.mp3")
