import os

from alg.hide_error import hide_alsa_error, redirect_error_output, restore_stderr
from alg.load_character import load_character
from alg.prompt.text_to_text_prompt import SYSTEM_PROMPT, USER_PROMPT
from db.access_db import save_conversation
from model.gpt_call import create_messages, gpt_call
from model.speech_call import speech_call
from model.speech_recognition_call import speech_recognition_call


def format_conversation(user: list[str], ai: list[str]) -> str:
    return "\n".join(
        [f"Child: {user[i]}\nYou: {ai[i]}" for i in range(min(len(user), len(ai)))]
    )


def sts_roop():
    audio_dir = "data/conversation3"
    os.makedirs(audio_dir, exist_ok=True)

    child_words = []
    ai_words = []

    visible = True
    while True:
        voice_text = speech_recognition_call()

        character = load_character()
        conversation = format_conversation(child_words, ai_words)

        messages = create_messages(
            SYSTEM_PROMPT,
            USER_PROMPT.format(
                conversation=conversation, input=voice_text, character=character
            ),
        )
        reponse_text = gpt_call(messages)

        speech_call(reponse_text, os.path.join(audio_dir, f"{voice_text}.mp3"))

        save_conversation(voice_text, reponse_text, visible)

        child_words.append(voice_text)
        ai_words.append(reponse_text)


def main():
    hide_alsa_error()
    stderr = redirect_error_output()
    sts_roop()
    restore_stderr(stderr)


if __name__ == "__main__":
    main()
