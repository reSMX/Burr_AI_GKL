import librosa
from pathlib import Path

from models import AudioFile


def trans_audio(path: Path):
    y, sr = librosa.load(path, mono=True, duration=30)

    return AudioFile(y=y, sr=sr)
