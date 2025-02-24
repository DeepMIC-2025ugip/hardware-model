import os

from alg.hide_error import hide_alsa_error, redirect_error_output, restore_stderr
from alg.llm_answer.answer import chat_answer
from alg.load_user_info import load_analysis, load_character, load_mental
from db.access_db import save_conversation
from model.speech_call import speech_call
from model.speech_recognition_call import speech_recognition_call

# from alg.prompt.text_to_text_prompt import SYSTEM_PROMPT, USER_PROMPT
# from model.gpt_call import gpt_call


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

        analysis, mental, character = load_analysis(), load_mental(), load_character()
        # conversation = format_conversation(child_words, ai_words)

        response_text = chat_answer(
            voice_text, analysis, mental, character, child_words, ai_words
        )
        # reponse_text = gpt_call(
        #     SYSTEM_PROMPT,
        #     USER_PROMPT.format(
        #         conversation=conversation, input=voice_text, character=character
        #     ),
        # )

        speech_call(response_text, os.path.join(audio_dir, f"{voice_text}.mp3"))

        save_conversation(voice_text, response_text, visible)

        child_words.append(voice_text)
        ai_words.append(response_text)


def main():
    hide_alsa_error()
    stderr = redirect_error_output()
    sts_roop()
    restore_stderr(stderr)


if __name__ == "__main__":
    main()
