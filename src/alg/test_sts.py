from alg.gpt_call import create_messages, gpt_call
from alg.hide_error import hide_alsa_error, redirect_error_output, restore_stderr
from alg.speech_call import speech_call
from alg.speech_recognition_call import speech_recognition_call


def sts_roop():
    while True:
        voice_text = speech_recognition_call()
        print(f"Speech To Text: {voice_text}")

        system_prompt = "You are the most intelligent person in the world."
        messages = create_messages(system_prompt, voice_text)
        reponse_text = gpt_call(messages)
        print(f"Text To Speech: {reponse_text}")
        speech_call(reponse_text, f"{voice_text}.mp3")

        if voice_text == "stop":
            print("The program is terminated.")
            break


if __name__ == "__main__":
    hide_alsa_error()
    stderr = redirect_error_output()
    sts_roop()
    restore_stderr(stderr)
