from fastapi import FastAPI
import numpy as np
from starlette.responses import JSONResponse
from librosa.feature import (
chroma_stft,
    rms,
    spectral_centroid,
    spectral_bandwidth,
    spectral_rolloff,
    zero_crossing_rate,
    mfcc
)

from audio_service import get
from models import AudioFile


app = FastAPI()


def to_np(y) -> np.array:
    return np.array(y)


@app.post("/libr_audio/")
async def get_audio(data: AudioFile) -> JSONResponse:
    y = to_np(data.y)
    sr = data.sr

    chroma_stf = chroma_stft(y=y, sr=sr)
    rmse = rms(y=y)
    spec_cent = spectral_centroid(y=y, sr=sr)
    spec_bw = spectral_bandwidth(y=y, sr=sr)
    rolloff = spectral_rolloff(y=y, sr=sr)
    zcr = zero_crossing_rate(y)
    mfc = mfcc(y=y, sr=sr)
    get_ = [ np.mean(rmse), np.mean(chroma_stf), np.mean(spec_cent),np.mean(spec_bw), np.mean(rolloff),np.mean(zcr)]
    for e in mfc:
        get_.append(np.mean(e))

    ans = int(get(get_)[0])

    return JSONResponse({
        "burr": ans
    })