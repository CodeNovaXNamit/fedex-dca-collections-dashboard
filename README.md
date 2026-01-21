📦 FedEx DCA Collections Dashboard with AI Prioritizer
🚀 Project Overview

FedEx works with multiple Debt Collection Agencies (DCAs) to recover overdue payments.
Currently, much of this process relies on manual spreadsheets and emails, which leads to slow recoveries, poor visibility, and inefficient prioritization.

This project is a prototype AI-powered collections dashboard that:

Centralizes overdue accounts

Uses a lightweight ML model to prioritize accounts by likelihood of payment

Provides a simple dashboard for monitoring and assignment

All data used in this project is synthetic and created for demonstration purposes only.


🎯 Key Features

📊 Centralized Dashboard for overdue accounts

🧠 AI Priority Score (0–1) indicating likelihood of payment

📋 Accounts table sorted by AI priority

🏷 Assign accounts to DCAs

📈 Aging bucket visualization (0–30, 31–60, 61–90, 90+)

⚡ Real-time updates via API


🧠 AI / Machine Learning

Model: Logistic Regression (scikit-learn)

Type: Supervised learning

Goal: Predict probability that an overdue account will pay in the next 30 days

Features used:

Amount due

Days overdue

Number of previous contacts

Evaluation metric: AUC

Achieved AUC = 0.987 on synthetic data

High score is expected due to controlled synthetic patterns

⚠️ The model is intended for prioritization, not absolute real-world prediction.

🏗 System Architecture
Streamlit Dashboard
        ↓
     Flask REST API
        ↓
SQLite Database + ML Model


Tech Stack:

Python 3.10+

Flask (backend API)

SQLite (database)

scikit-learn (ML model)

Streamlit (dashboard UI)

pandas, joblib

📂 Project Structure
fedex-dca-collections-dashboard/
├── app.py                  # Flask backend
├── streamlit_app.py        # Streamlit dashboard
├── requirements.txt
├── README.md
├── data/
│   └── accounts_with_labels.csv
├── models/
│   └── prioritizer.joblib
├── scripts/
│   ├── generate_data.py
│   ├── train_model.py
│   └── init_db.py
├── db/
│   └── accounts.db
└── .gitignore

⚙️ How to Run the Project (Local)
1️⃣ Clone the repository
git clone <your-repo-url>
cd fedex-dca-collections-dashboard

2️⃣ Create and activate virtual environment

Windows

python -m venv venv
venv\Scripts\activate


macOS / Linux

python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Generate synthetic data
python scripts/generate_data.py

5️⃣ Train the ML model
python scripts/train_model.py

6️⃣ Initialize the database
python scripts/init_db.py

7️⃣ Run backend (Flask)
python app.py


Backend runs at:
👉 http://127.0.0.1:5000

8️⃣ Run dashboard (Streamlit)

Open a new terminal (venv activated):

streamlit run streamlit_app.py


Dashboard opens at:
👉 http://localhost:8501

📊 Dashboard Capabilities

View KPIs (total overdue, open accounts, avg overdue days)

See accounts ranked by AI priority score

Assign accounts to agencies

Visualize aging buckets

Validate AI-driven prioritization

👥 Team Roles

Backend & AI: Flask API, SQLite, ML model

Dashboard & UX: Streamlit UI and visualizations

Business & Documentation: PPT, README, demo flow

📌 Data Disclaimer

All data used in this project is synthetically generated for hackathon demonstration purposes.
No real FedEx customer, invoice, or payment data was used.

🔮 Future Enhancements

Integration with real enterprise data

Role-based access control (RBAC)

Automated model retraining

DCA performance analytics

Cloud deployment