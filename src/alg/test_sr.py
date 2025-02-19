from alg.hide_error import hide_alsa_error, redirect_error_output, restore_stderr
from alg.speech_recognition_call import speech_recognition_call


def stt_roop():
    while True:
        voice_text = speech_recognition_call()
        if voice_text == "stop":
            print("The program is terminated.")
            break


if __name__ == "__main__":
    hide_alsa_error()
    stderr = redirect_error_output()
    stt_roop()
    restore_stderr(stderr)
