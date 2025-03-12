import librosa
from fastapi import FastAPI
from librosa.feature import (
    rms,
    chroma_stft,
    mfcc
)
import numpy as np
from tensorflow.keras.models import load_model
from models import AudioFile
model = load_model('backend/learn_model/model.keras.keras')
app = FastAPI()
@app.get("/libr_audio/")
async  def get_audio(data: AudioFile):
    y = data.y
    sr = data.sr
    y, index = librosa.effects.trim(y)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    get = [ np.mean(rmse), np.mean(chroma_stft), np.mean(spec_cent),np.mean(spec_bw), np.mean(rolloff),np.mean(zcr)]
    for e in mfcc:
        get.append(np.mean(e))
    predict = model.pedict(get)


    return predict