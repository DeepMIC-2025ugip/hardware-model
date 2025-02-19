import io

from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

from alg.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


def speech_call(
    input_text: str,
    save_file: str,
    audio_format: str = "mp3",
    model: str = "tts-1",
    voice: str = "nova",
):
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text,
    )

    byte_stream = io.BytesIO(response.content)
    audio = AudioSegment.from_file(byte_stream, format=audio_format)

    play(audio)

    audio.export(save_file, format=audio_format)

    return response


if __name__ == "__main__":
    input_text = input("Q: ")
    save_file = f"{input_text}.mp3"
    speech_call(input_text, save_file)
    print("The audio file is saved.")
