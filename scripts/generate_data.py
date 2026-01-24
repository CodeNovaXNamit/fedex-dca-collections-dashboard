import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

N = 5000  # number of synthetic accounts

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
def payment_probability(row):
    prob = 0.5  # base probability

    # Amount effect (lower amount → higher chance)
    if row["amount_due"] < 300:
        prob += 0.25
    elif row["amount_due"] < 700:
        prob += 0.10
    else:
        prob -= 0.20

    # Days overdue effect (fewer days → higher chance)
    if row["days_overdue"] < 30:
        prob += 0.30
    elif row["days_overdue"] < 90:
        prob += 0.10
    else:
        prob -= 0.25

    # Contact fatigue effect
    if row["num_previous_contacts"] > 3:
        prob -= 0.15

    # Add noise (real-world uncertainty)
    prob += np.random.normal(0, 0.1)

    # Clamp probability between 0 and 1
    return max(0, min(1, prob))


# Generate probabilistic labels
df["payment_probability"] = df.apply(payment_probability, axis=1)
df["label_paid_next_month"] = (
    np.random.rand(len(df)) < df["payment_probability"]
).astype(int)


# Save dataset
df.to_csv("data/accounts_with_labels.csv", index=False)

print("✅ Synthetic data generated: data/accounts_with_labels.csv")
