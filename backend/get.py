import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

def predict(model, features_list):
    features_df = pd.DataFrame([features_list])
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_df)
    return model.predict(features_scaled)

# Пример использования
def get(input_features):
    model = joblib.load('learn_model/audio_classifier_model.joblib')
    return  predict(model, input_features)