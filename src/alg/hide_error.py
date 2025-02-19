import logging
import os
import warnings


def hide_alsa_error():
    # ALSAとPyAudioの警告を抑制
    logging.getLogger("ALSA").setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # ALSA lib関連のエラーメッセージを/dev/nullにリダイレクト
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


def redirect_error_output():
    stderr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_WRONLY)
    return stderr


def restore_stderr(stderr):
    os.close(2)
    os.dup2(stderr, 2)
    os.close(stderr)
