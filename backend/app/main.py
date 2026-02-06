import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

timestamps = {
    "00-11-22-33-44-55": ["2024-01-01T10:00:00Z", "2024-01-01T10:02:00Z"],
    "00-11-22-33-44-56": ["2024-01-01T10:05:00Z", "2024-01-01T10:07:00Z"],
    "00-11-22-33-44-57": ["2024-01-01T10:10:00Z", "2024-01-01T10:12:00Z"],
    "00-11-22-33-44-58": ["2024-01-01T10:15:00Z", "2024-01-01T10:17:00Z"],
    "00-11-22-33-44-A5": ["2024-01-02T11:00:00Z", "2024-01-02T11:02:00Z"],
    "00-11-22-33-44-A6": ["2024-01-02T11:05:00Z", "2024-01-02T11:07:00Z"],
    "00-11-22-33-44-A7": ["2024-01-02T11:10:00Z", "2024-01-02T11:12:00Z"],
    "00-11-22-33-44-A8": ["2024-01-02T11:15:00Z", "2024-01-02T11:17:00Z"],
}

drivers = {
    1: [{"id": 1, "name": "Niklas Maderbacher"}],
    2: [{"id": 2, "name": "Driver Two"}],
}

@app.route('/api/teams/', methods=['GET'])
def get_teams():
    # Dummy data for teams
    teams = [
        {"id": 1, "name": "ZEC Team"},
        {"id": 2, "name": "Team B"},
    ]
    return jsonify(teams)

@app.route("/api/challenges/", methods=["GET"])
def get_challenges():
    # Dummy data for challenges
    challenges = [
        {"id": 1, "name": "Slalom", "esp_mac_start1": "00-11-22-33-44-55", "esp_mac_start2": "00-11-22-33-44-56", "esp_mac_finish1": "00-11-22-33-44-57", "esp_mac_finish2": "00-11-22-33-44-58"},
        {"id": 2, "name": "Skidpad", "esp_mac_start1": "00-11-22-33-44-A5", "esp_mac_start2": "00-11-22-33-44-A6", "esp_mac_finish1": "00-11-22-33-44-A7", "esp_mac_finish2": "00-11-22-33-44-A8"},
    ]
    return jsonify(challenges)

@app.route("/api/penalties/", methods=["GET"])
def get_penalties():
    # Dummy data for penalties
    penalties = [
        {"id": 1, "amount": 5, "type": "Strecke Verlassen"},
        {"id": 2, "amount": 10, "type": "Hüterl nieder"},
    ]
    return jsonify(penalties)

@app.route("/api/drivers/<team_id>", methods=["GET"])
def get_drivers(team_id):
    team_drivers = drivers.get(int(team_id), [])
    return jsonify(team_drivers)

@app.route("/api/timestamps/<mac_address>", methods=["GET"])
def get_timestamps(mac_address):
    timestamp = timestamps[mac_address]

    return jsonify({"timestamp": timestamp})
