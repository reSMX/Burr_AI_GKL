import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

try:
    df = pd.read_csv('database.csv')
except FileNotFoundError:
    print("Ошибка: CSV файл 'database.csv' не найден.")
    exit()

X = df.drop('class', axis=1)
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

model_filename = 'audio_classifier_model.joblib'
joblib.dump(model, model_filename)
print(f"Модель сохранена в файл: {model_filename}")

loaded_model = joblib.load(model_filename)
print("Модель загружена.")

y_pred = loaded_model.predict(X_test)

print("\nОценка качества модели (загруженной):")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=loaded_model.classes_, yticklabels=loaded_model.classes_)
plt.xlabel('Предсказанные классы')
plt.ylabel('Фактические классы')
plt.title('Confusion Matrix')
plt.show()