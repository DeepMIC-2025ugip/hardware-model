from typing import Union

import speech_recognition as sr

listener = sr.Recognizer()
THRESHOLD = 2000


def speech_recognition_call() -> Union[str, None]:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            listener.energy_threshold = THRESHOLD
            voice = listener.listen(source)
            voice_text = listener.recognize_google(voice, language="ja-JP")
            print(f"text: {voice_text}")
            return voice_text

    except sr.UnknownValueError:
        print("Cannnot recognize the voice.")
        return None
    except sr.RequestError:
        print("Failed to connect to Google service.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# TODO: backgroundで音声認識を行う関数のバグ修正
def callback(recognizer, audio):
    """音声を取得するたびに実行されるコールバック関数"""
    try:
        voice_text = recognizer.recognize_google(audio, language="ja-JP")
        print(f"text: {voice_text}")
        if voice_text == "stop":
            print("The program is terminated.")
            exit(0)  # プログラムを終了する
    except sr.UnknownValueError:
        print("Cannot recognize the voice.")
    except sr.RequestError:
        print("Failed to connect to Google service.")
    except Exception as e:
        print(f"Error: {e}")


def stt_roop():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        listener.energy_threshold = THRESHOLD
        print("Listening...")
        stop_listening = listener.listen_in_background(source, callback)

        try:
            while True:
                pass  # メインスレッドを維持（何か他の処理を入れてもOK）
        except KeyboardInterrupt:
            stop_listening(wait_for_stop=False)
            print("Stopped listening.")
