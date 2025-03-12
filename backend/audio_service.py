import joblib
import pandas as pd
import librosa
from pathlib import Path
from sklearn.preprocessing import StandardScaler


def predict(model, features_list):
    features_df = pd.DataFrame([features_list])
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_df)
    return model.predict(features_scaled)


def get(input_features):
    model = joblib.load('learn_model/audio_classifier_model.joblib')
    return predict(model, input_features)


def trans_audio(path: Path):
    y, sr = librosa.load(path, mono=True, duration=30)
    y = y.astype(float).tolist()

    return y, sr
