# import pickle
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
# import matplotlib.pyplot as plt
# from collections import Counter

# # Load extracted features from travel/emergency dataset
# with open('./video_travel_emergency_data.pickle', 'rb') as f:
#     data_dict = pickle.load(f)

# data = np.asarray(data_dict['data'])   # (samples, 84)
# labels = np.asarray(data_dict['labels'])

# # Get sorted unique class labels
# word_classes = sorted(list(set(labels)))

# print("📚 Classes found in dataset:", word_classes)
# print("🔢 Sample count per class:", dict(Counter(labels)))

# # Split data for training and testing
# x_train, x_test, y_train, y_test = train_test_split(
#     data, labels, test_size=0.2, random_state=42, stratify=labels
# )

# # Train Random Forest model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(x_train, y_train)

# # Evaluate the model
# y_predict = model.predict(x_test)
# accuracy = accuracy_score(y_test, y_predict)
# print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")

# # Plot confusion matrix
# cm = confusion_matrix(y_test, y_predict, labels=word_classes)
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=word_classes)
# disp.plot(xticks_rotation=45, cmap='Blues')
# plt.title("Confusion Matrix - Travel & Emergency Classifier")
# plt.tight_layout()
# plt.show()

# # Save the trained model
# with open('video_travel_emergency_model.p', 'wb') as f:
#     pickle.dump({'model': model, 'classes': word_classes}, f)

# print("💾 Model trained and saved as 'video_travel_emergency_model.p'")



import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from collections import Counter

# Load extracted features from travel/emergency dataset
with open('./video_communication_data.pickle', 'rb') as f:
    data_dict = pickle.load(f)

data = np.asarray(data_dict['data'])   # (samples, 84)
labels = np.asarray(data_dict['labels'])

# Get sorted unique class labels
word_classes = sorted(list(set(labels)))

print("📚 Classes found in dataset:", word_classes)
print("🔢 Sample count per class:", dict(Counter(labels)))

# Split data for training and testing
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=42, stratify=labels
)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# ✅ NEW: Check for overfitting/underfitting
train_accuracy = model.score(x_train, y_train)
test_accuracy = model.score(x_test, y_test)

print(f"\n📈 Training Accuracy: {train_accuracy * 100:.2f}%")
print(f"🧪 Testing Accuracy: {test_accuracy * 100:.2f}%")

# Evaluate the model
y_predict = model.predict(x_test)
accuracy = accuracy_score(y_test, y_predict)
print(f"\n✅ Overall Test Accuracy: {accuracy * 100:.2f}%")

# Plot confusion matrix
cm = confusion_matrix(y_test, y_predict, labels=word_classes)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=word_classes)
disp.plot(xticks_rotation=45, cmap='Blues')
plt.title("Confusion Matrix - Greetings & Communication Classifier")
plt.tight_layout()
plt.show()

# Save the trained model
with open('video_communication_model.p', 'wb') as f:
    pickle.dump({'model': model, 'classes': word_classes}, f)

print("💾 Model trained and saved as 'video_travel_emergency_model.p'")
