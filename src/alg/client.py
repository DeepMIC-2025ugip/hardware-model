import asyncio

import numpy as np
import sounddevice as sd
import websockets

URL = "ws://localhost:8000/api/stt/"
DEVICE_INDEX = 3  # USBマイク（Webcam）のデバイスインデックス


async def send_audio():
    queue = asyncio.Queue()

    async with websockets.connect(URL) as websocket:

        def callback(indata, frames, time, status):
            if status:
                print(f"Sounddevice status: {status}")
            queue.put_nowait(indata.copy())

        stream = sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype=np.int16,
            callback=callback,
            device=DEVICE_INDEX,  # USBマイクを指定
        )

        print("🎤 音声ストリーム開始（USBマイク）")
        with stream:
            while True:
                try:
                    indata = await queue.get()
                    await websocket.send(indata.tobytes())  # 音声データを送信
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"エラー: {e}")
                    break


if __name__ == "__main__":
    try:
        asyncio.run(send_audio())
    except KeyboardInterrupt:
        print("プログラムが中断されました")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
