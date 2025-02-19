import logging
import os
import warnings

import speech_recognition as sr

listener = sr.Recognizer()
THRESHOLD = 2000


def hide_alsa_error():
    # ALSAとPyAudioの警告を抑制
    logging.getLogger("ALSA").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # ALSA lib関連のエラーメッセージを/dev/nullにリダイレクト
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


def redirect_error_output():
    stderr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_WRONLY)
    return stderr


def restore_stderr(stderr):
    os.close(2)
    os.dup2(stderr, 2)
    os.close(stderr)


def stt_roop(listener: sr.Recognizer):
    try:
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    listener.adjust_for_ambient_noise(source)
                    listener.energy_threshold = THRESHOLD
                    voice = listener.listen(source)
                    voice_text = listener.recognize_google(voice, language="ja-JP")
                    print(f"text: {voice_text}")

            except sr.UnknownValueError:
                print("Cannnot recognize the voice.")
            except sr.RequestError:
                print("Failed to connect to Google service.")
            except Exception as e:
                print(f"Error: {e}")

    finally:
        restore_stderr()


if __name__ == "__main__":
    hide_alsa_error()
    stderr = redirect_error_output()
    stt_roop(listener)
