import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from catboost import CatBoostClassifier, Pool

try:
    df = pd.read_csv('database.csv')
except FileNotFoundError:
    print("Ошибка: CSV файл 'database.csv' не найден.")
    exit()

X = df.drop('class', axis=1)
y = df['class']

model = CatBoostClassifier(iterations=3,
                           depth=6,
                           learning_rate=1,
                           loss_function='Logloss',
                           verbose=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
model.fit(X_train, y_train)
test_data = catboost_pool = Pool(X_test,
                                 y_test)

# model = RandomForestClassifier(random_state=42)
# model.fit(X_train, y_train)

model_filename = 'audio_classifier_model.joblib'
joblib.dump(model, model_filename)
print(f"Модель сохранена в файл: {model_filename}")

loaded_model = joblib.load(model_filename)
print("Модель загружена.")

preds_class = model.predict(test_data)
preds_proba = model.predict_proba(test_data)
print("class = ", preds_class)
print("proba = ", preds_proba)
