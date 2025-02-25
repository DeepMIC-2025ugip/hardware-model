import os
import random
import subprocess

def play_background_music(music_dir):
    """ 指定したディレクトリの音楽ファイルをランダムに再生 """
    music_files = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        return None  # 音楽ファイルがなければ何もしない

    music_path = os.path.join(music_dir, random.choice(music_files))
    process = subprocess.Popen(["mpg123", "-q", music_path])  # `mpg123` で再生
    return process


def stop_background_music(process):
    """ 音楽再生プロセスを停止 """
    if process:
        process.terminate()
