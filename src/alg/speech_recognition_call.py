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
