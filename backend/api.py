import librosa
from fastapi import FastAPI
from librosa.feature import (
    rms,
    chroma_stft,
    mfcc
)
import numpy as np
from starlette.responses import JSONResponse

from get import get
from models import AudioFile


app = FastAPI()


def to_np(y) -> np.array:
    return np.array(y)


@app.post("/libr_audio/")
async  def get_audio(data: AudioFile) -> JSONResponse:
        y = to_np(data.y)
        sr = data.sr

        chroma_stf = chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfc = mfcc(y=y, sr=sr)
        get_ = [ np.mean(rmse), np.mean(chroma_stf), np.mean(spec_cent),np.mean(spec_bw), np.mean(rolloff),np.mean(zcr)]
        for e in mfc:
            get_.append(np.mean(e))

        ans = int(get(get_)[0])

        return JSONResponse({
            "burr": ans
        })