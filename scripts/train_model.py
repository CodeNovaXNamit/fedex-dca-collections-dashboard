import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib
import os

# Load dataset
df = pd.read_csv("data/accounts_with_labels.csv")

# Feature selection
FEATURES = [
    "amount_due",
    "days_overdue",
    "num_previous_contacts"
]

X = df[FEATURES]
y = df["label_paid_next_month"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_proba)

print(f"✅ Model trained successfully")
print(f"📊 AUC Score: {auc:.3f}")

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, "models/prioritizer.joblib")
print("💾 Model saved to models/prioritizer.joblib")
