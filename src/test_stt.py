import contextlib
import time

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Whisperモデルのロード（Raspberry Pi 5 の CPU 用に int8 設定）
# model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
model = WhisperModel("tiny", device="cpu")

# USBマイクのデバイス番号を指定（arecord -l で確認）
DEVICE_INDEX = 3  # C970 USBマイク
SAMPLE_RATE = 16000  # Whisper が期待するサンプリングレート
BUFFER_DURATION = 3  # 5秒ごとに文字起こし

# ノイズを検出するためのしきい値
THRESHOLD = 0.01  # 例えば、0.01以下の振幅は無視


@contextlib.contextmanager
def timer():
    """処理時間を計測するコンテキストマネージャ"""
    start = time.monotonic()
    yield
    end = time.monotonic()
    print(f"⏱️ 文字起こし時間: {end - start:.3f} 秒")


def callback(indata, frames, time, status):
    """音声入力のコールバック関数（データをバッファに格納）"""
    if status:
        print(f"⚠️ Sounddevice status: {status}")
    # ノイズしきい値以下のデータをフィルタリング
    filtered_data = indata[:, 0]
    if np.max(np.abs(filtered_data)) > THRESHOLD:
        audio_buffer.extend(filtered_data)  # モノラルデータのみ取得


if __name__ == "__main__":
    audio_buffer = []

    print("🎤 音声文字起こしを開始します（USBマイク）")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16,
        callback=callback,
        device=DEVICE_INDEX,
    ):
        while True:
            try:
                if len(audio_buffer) >= SAMPLE_RATE * BUFFER_DURATION:
                    with timer():
                        # int16 -> float32 変換
                        audio_data = (
                            np.array(audio_buffer, dtype=np.int16).astype(np.float32)
                            / 32768.0
                        )
                        audio_buffer = []  # バッファをリセット

                        # 文字起こし処理時間を計測
                        segments, _ = model.transcribe(audio_data, language="ja")

                    text = "".join(segment.text for segment in segments)
                    print(f"📝 文字起こし結果: {text}")

            except KeyboardInterrupt:
                print("\n🛑 プログラムを終了します")
                break
            except Exception as e:
                print(f"⚠️ エラー: {e}")
