from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DB_NAME = "sos.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sos_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()


def log_activity(action):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO activity_log (action, timestamp) VALUES (?, ?)",
        (action, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()


@app.route("/hello", methods=["GET"])
def home():
    return jsonify({"status": "Her Guard Backend Running"})


@app.route("/sos", methods=["POST"])
def sos_alert():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat is None or lon is None:
        return jsonify({"error": "Location missing"}), 400

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sos_alerts (latitude, longitude, timestamp) VALUES (?, ?, ?)",
        (lat, lon, time_now)
    )
    conn.commit()
    conn.close()

    log_activity("SOS activated")

    return jsonify({
        "message": "SOS Activated",
        "maps_link": f"https://www.google.com/maps?q={lat},{lon}",
        "time": time_now
    })


@app.route("/share-location", methods=["POST"])
def share_location():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat is None or lon is None:
        return jsonify({"error": "Location missing"}), 400

    log_activity("Location shared")

    return jsonify({
        "message": "Location shared successfully",
        "maps_link": f"https://www.google.com/maps?q={lat},{lon}"
    })

@app.route("/recent-activity", methods=["GET"])
def recent_activity():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT action, timestamp
        FROM activity_log
        ORDER BY id DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    conn.close()

    activity = []
    for r in rows:
        activity.append({
            "action": r[0],
            "time": r[1]
        })

    return jsonify(activity)


@app.route("/recent-alerts", methods=["GET"])
def recent_alerts():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT latitude, longitude, timestamp
        FROM sos_alerts
        ORDER BY id DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    conn.close()

    alerts = []
    for r in rows:
        alerts.append({
            "latitude": r[0],
            "longitude": r[1],
            "time": r[2]
        })

    return jsonify(alerts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)