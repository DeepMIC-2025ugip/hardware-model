import asyncio

import numpy as np
import sounddevice as sd
from fastapi import APIRouter, WebSocket
from faster_whisper import WhisperModel

router = APIRouter()

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 接続開始")

    try:
        while True:
            data = await websocket.receive_bytes()
            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

            segments, _ = model.transcribe(audio, language="ja")

            text = "".join(segment.text for segment in segments)
            await websocket.send_text(text)

    except Exception as e:
        print(f"エラー: {e}")
    finally:
        await websocket.close()
