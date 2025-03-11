import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
if tf.config.list_physical_devices('GPU'):
    device_name = tf.test.gpu_device_name()
    if device_name != '/device:GPU:0':
        print('GPU device found: {}'.format(device_name))
    else:
        print("GPU device not found")
else:
    print("No GPU found, using CPU.")

data = pd.read_csv('database.csv')
X = data.drop('class', axis=1)
y = data['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train_scaled_np = np.array(X_train_scaled).astype(np.float32)
X_test_scaled_np = np.array(X_test_scaled).astype(np.float32)
y_train_np = np.array(y_train).astype(np.float32)
y_test_np = np.array(y_test).astype(np.float32)


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train_scaled_np.shape[1],)),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()

with tf.device(device_name if tf.config.list_physical_devices('GPU') else '/CPU:0'):
    print("Training on:", device_name if tf.config.list_physical_devices('GPU') else 'CPU')
    history = model.fit(X_train_scaled_np, y_train_np,
                        epochs=50,
                        batch_size=32,
                        validation_data=(X_test_scaled_np, y_test_np),
                        verbose=1)

model.save('model.keras')

with tf.device(device_name if tf.config.list_physical_devices('GPU') else '/CPU:0'):
    loss, accuracy = model.evaluate(X_test_scaled_np, y_test_np, verbose=0)
    print(f"Test Accuracy: {accuracy:.4f}")

    y_prob = model.predict(X_test_scaled_np).flatten()
    y_pred_np = np.where(y_prob >= 0.5, 1, 0)


print("\nClassification Report:")
print(classification_report(y_test_np, y_pred_np))

cm = confusion_matrix(y_test_np, y_pred_np)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Нет картавости', 'Есть картавости'],
            yticklabels=['Нет картавости', 'Есть картавости'])
plt.xlabel('Предсказанный класс')
plt.ylabel('Реальный класс')
plt.title('Матрица ошибок (TensorFlow)')
plt.show()

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Точность на обучающей выборке')
plt.plot(history.history['val_accuracy'], label='Точность на валидационной выборке')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.legend()
plt.title('Точность модели')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Потери на обучающей выборке')
plt.plot(history.history['val_loss'], label='Потери на валидационной выборке')
plt.xlabel('Эпоха')
plt.ylabel('Потери')
plt.legend()
plt.title('Потери модели')
plt.tight_layout()
plt.show()