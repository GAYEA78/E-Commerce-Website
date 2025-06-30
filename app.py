from flask import Flask, jsonify
import sqlite3
import subprocess

app = Flask(__name__)

DATABASE = "northwind.db"

@app.route("/")
def index():
    return "Northwind API is running!"

@app.route("/report")
def report():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        with open("report.sql", "r") as f:
            query = f.read()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update")
def update():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        with open("update.sql", "r") as f:
            updates = f.read().split(";")
        for statement in updates:
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        conn.close()
        return jsonify({"status": "Updates applied successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/populate")
def populate():
    try:
        subprocess.run(["python", "populate.py"], check=True)
        return jsonify({"status": "Database repopulated successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
 