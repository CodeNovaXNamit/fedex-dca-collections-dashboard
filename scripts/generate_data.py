import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

N = 500  # number of synthetic accounts

df = pd.DataFrame({
    "account_id": [f"A{1000+i}" for i in range(N)],
    "customer_name": [f"Customer_{i}" for i in range(N)],
    "amount_due": np.round(np.random.exponential(scale=500, size=N), 2),
    "days_overdue": np.random.randint(1, 180, size=N),
    "num_previous_contacts": np.random.poisson(lam=1.5, size=N),
    "agency_assigned": np.random.choice(
        ["AgencyX", "AgencyY", "AgencyZ", None], size=N, p=[0.3, 0.3, 0.2, 0.2]
    ),
    "status": np.random.choice(
        ["open", "in-progress", "closed"], size=N, p=[0.6, 0.25, 0.15]
    )
})

# Synthetic label logic:
# Higher chance to pay if amount and days overdue are low
df["label_paid_next_month"] = (
    (df["amount_due"] < 400) &
    (df["days_overdue"] < 60)
).astype(int)

# Save dataset
df.to_csv("data/accounts_with_labels.csv", index=False)

print("✅ Synthetic data generated: data/accounts_with_labels.csv")
