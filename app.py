from flask import Flask, render_template, request
import sqlite3
import joblib
from scipy.sparse import hstack

app = Flask(__name__)

# Load AI detector
pkg = joblib.load("sqli_detector.pkl")
model = pkg["model"]
vectorizer = pkg["vectorizer"]

def detect_sqli(payload):
    vec = vectorizer.transform([payload])

    features = [[
        len(payload),
        sum(1 for c in payload if not c.isalnum() and not c.isspace()),
        payload.count("'"),
        payload.count("="),
        payload.count("-")
    ]]

    combined = hstack([vec, features])
    proba = model.predict_proba(combined)[0][1]

    return proba > 0.6  # threshold

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if detect_sqli(username) or detect_sqli(password):
            message = "🚨 SQL Injection Detected!"
            return render_template("login.html", message=message)
# this query is vuln to SQLI as we put the input directly into the app
        query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
        """

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        conn.close()

        if result:
            message = f"✅ Welcome {result[1]}"
        else:
            message = "❌ Invalid credentials"

    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(debug=True,port=8889)
