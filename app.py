from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

DB_PATH = "db/accounts.db"

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# API: Get all accounts
# -------------------------
@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM accounts", conn)
    conn.close()

    return jsonify(df.to_dict(orient="records"))

# -------------------------
# API: Get single account
# -------------------------
@app.route("/api/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(dict(row))

# -------------------------
# API: Assign account to agency
# -------------------------
@app.route("/api/accounts/<int:account_id>/assign", methods=["PUT"])
def assign_account(account_id):
    data = request.get_json()
    agency = data.get("agency")

    if not agency:
        return jsonify({"error": "Agency is required"}), 400

    conn = get_db_connection()
    conn.execute(
        "UPDATE accounts SET agency_assigned = ? WHERE id = ?",
        (agency, account_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Account assigned successfully"})
if __name__ == "__main__":
    app.run(debug=True)
