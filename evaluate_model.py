import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

# Load data
X_dataset = np.loadtxt('model/keypoint_classifier/keypoint.csv', delimiter=',', dtype='float32', usecols=list(range(1, (21 * 2) + 1)))
y_dataset = np.loadtxt('model/keypoint_classifier/keypoint.csv', delimiter=',', dtype='int32', usecols=(0))

print(f"Dataset shape: {X_dataset.shape}")
print(f"Labels shape: {y_dataset.shape}")
print(f"Classes: {np.unique(y_dataset)}")
print(f"Class counts: {[np.sum(y_dataset==i) for i in np.unique(y_dataset)]}")

# Load model
model = tf.keras.models.load_model('model/keypoint_classifier/keypoint_classifier_vit.h5')

# Simple evaluation on full dataset
predictions = model.predict(X_dataset)
pred_classes = np.argmax(predictions, axis=1)

print('\nClassification Report:')
print(classification_report(y_dataset, pred_classes))

print('Confusion Matrix:')
print(confusion_matrix(y_dataset, pred_classes))