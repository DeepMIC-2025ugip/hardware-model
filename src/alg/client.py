import asyncio

import numpy as np
import sounddevice as sd
import websockets

URL = "ws://localhost:8000/api/stt"


async def send_audio():
    async with websockets.connect(URL) as websocket:

        def callback(indata, frames, time, status):
            if status:
                print(status)
            asyncio.create_task(websocket.send(indata.tobytes()))

        with sd.InputStream(
            samplerate=16000, channels=1, dtype=np.int16, callback=callback
        ):
            await asyncio.Future()  # 永久ループ


asyncio.run(send_audio())
