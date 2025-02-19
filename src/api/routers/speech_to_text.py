import numpy as np
from fastapi import APIRouter, WebSocket
from faster_whisper import WhisperModel

router = APIRouter()

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    print(f"WebSocket connection attempt from {websocket.client}")
    try:
        await websocket.accept()
        print("✅ WebSocket 接続開始")
    except Exception as e:
        print(f"WebSocket接続エラー: {e}")
        raise

    try:
        while True:
            data = await websocket.receive_bytes()
            audio = (
                np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            )  # int16 → float32 変換

            print(f"📢 受信データ: {audio.shape}, dtype={audio.dtype}")

            segments, _ = model.transcribe(audio, language="ja")

            text = "".join(segment.text for segment in segments)
            print(f"📝 文字起こし結果: {text}")

            await websocket.send_text(text)

    except Exception as e:
        print(f"エラー: {e}")
    finally:
        await websocket.close()
