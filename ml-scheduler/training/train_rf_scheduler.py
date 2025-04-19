import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data
with open("dataset/training/uniform_train.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Binary label: 1 if short job, 0 if long job
median_burst = df["burst_time"].median()
df["label"] = df["burst_time"].apply(lambda x: 1 if x < median_burst else 0)

# Features
X = df[["arrival_time", "burst_time", "priority"]]
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

# Save
joblib.dump(model, "schedulers/rf_model.pkl")