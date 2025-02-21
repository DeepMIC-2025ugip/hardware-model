import os

from model.gpt_call import create_messages, gpt_call
from alg.hide_error import hide_alsa_error, redirect_error_output, restore_stderr
from alg.prompt.text_to_text_prompt import SYSTEM_PROMPT, USER_PROMPT
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
    return_words = []

    while True:
        voice_text = speech_recognition_call()

        conversation = format_conversation(child_words, return_words)
        messages = create_messages(
            SYSTEM_PROMPT,
            USER_PROMPT.format(conversation=conversation, input=voice_text),
        )
        reponse_text = gpt_call(messages)
        speech_call(reponse_text, os.path.join(audio_dir, f"{voice_text}.mp3"))

        child_words.append(voice_text)
        return_words.append(reponse_text)


if __name__ == "__main__":
    hide_alsa_error()
    stderr = redirect_error_output()
    sts_roop()
    restore_stderr(stderr)
