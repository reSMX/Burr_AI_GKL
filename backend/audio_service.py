import pandas as pd
import librosa
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from catboost import CatBoostClassifier, Pool


def predict(model, features_list):
    features_df = pd.DataFrame([features_list])
    scaler = MinMaxScaler(feature_range=(-1, 1))
    features_scaled = scaler.fit_transform(features_df)
    pool = Pool(data=features_scaled)
    return model.predict(pool)


def get(input_features):
    model = CatBoostClassifier()
    model.load_model('learn_model/audio_classifier_model.cbm')
    return predict(model, input_features)


def trans_audio(path: Path):
    y, sr = librosa.load(path, mono=True, duration=30)
    y = y.astype(float).tolist()

    return y, sr
