import io

from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

from settings import settings

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

    audio.export(save_file, format=audio_format)
    
    play(audio)

    return audio


if __name__ == "__main__":
    input_text = input("Q: ")
    save_file = f"data/music/{input_text}.mp3"
    audio = speech_call(input_text, save_file)
    play(audio)
    print("The audio file is saved.")
