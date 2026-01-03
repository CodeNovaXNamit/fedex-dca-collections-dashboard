import sqlite3
import pandas as pd
import joblib
from datetime import datetime

# Paths
DB_PATH = "db/accounts.db"
DATA_PATH = "data/accounts_with_labels.csv"
MODEL_PATH = "models/prioritizer.joblib"

# Load ML model
model = joblib.load(MODEL_PATH)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT,
    customer_name TEXT,
    amount_due REAL,
    days_overdue INTEGER,
    num_previous_contacts INTEGER,
    agency_assigned TEXT,
    status TEXT,
    predicted_score REAL,
    last_updated TIMESTAMP
)
""")

# Load CSV data
df = pd.read_csv(DATA_PATH)

# Compute predicted score for each row
def compute_score(row):
    X = pd.DataFrame([{
        "amount_due": row["amount_due"],
        "days_overdue": row["days_overdue"],
        "num_previous_contacts": row["num_previous_contacts"]
    }])
    return float(model.predict_proba(X)[:, 1][0])

df["predicted_score"] = df.apply(compute_score, axis=1)
df["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Insert data into DB
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO accounts (
            account_id, customer_name, amount_due, days_overdue,
            num_previous_contacts, agency_assigned, status,
            predicted_score, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["account_id"],
        row["customer_name"],
        row["amount_due"],
        int(row["days_overdue"]),
        int(row["num_previous_contacts"]),
        row["agency_assigned"],
        row["status"],
        row["predicted_score"],
        row["last_updated"]
    ))

conn.commit()
conn.close()

print("✅ Database initialized and data loaded into db/accounts.db")
