import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/")
async def tts(text: str):
    """テキストを音声に変換"""
    pass
    # tts = edge_tts.Communicate(text, voice="ja-JP-NanamiNeural")
    # stream = await tts.stream()

    # async def audio_stream():
    #     async for chunk in stream:
    #         yield chunk

    # return StreamingResponse(audio_stream(), media_type="audio/wav")
