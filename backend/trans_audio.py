import librosa
from pathlib import Path

from backend.models import AudioFile


def trans_audio(path: Path):
    y, sr = librosa.load(path, mono=True, duration=30)
    y = y.astype(float).tolist()
    return y, sr