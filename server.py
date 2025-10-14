import sqlite3
import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB_NAME = 'game.db'

def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # This makes the data easier to work with
    return conn

# API endpoint to get a random scenario
@app.route("/api/get_scenario")
def api_get_scenario():
    conn = get_db_connection()
    scenarios = conn.execute("SELECT * FROM scenarios").fetchall()
    conn.close()

    if scenarios:
        random_scenario = random.choice(scenarios)
        return jsonify(dict(random_scenario))
    return jsonify({"error": "No scenarios found."}), 404

# NEW: API endpoint to check a player's answer
@app.route("/api/submit_answer", methods=['POST'])
def api_submit_answer():
    # Get the data sent by the game (e.g., {"scenario_id": 1, "choice": "BUY"})
    data = request.get_json()
    scenario_id = data.get('scenario_id')
    player_choice = data.get('choice')

    conn = get_db_connection()
    scenario = conn.execute("SELECT * FROM scenarios WHERE scenario_id = ?", (scenario_id,)).fetchone()
    conn.close()

    if not scenario:
        return jsonify({"error": "Scenario not found."}), 404

    is_correct = (player_choice == scenario['correct_answer'])

    if is_correct:
        response = {
            "correct": True,
            "feedback": scenario['win_feedback'],
            "amount": scenario['win_amount']
        }
    else:
        response = {
            "correct": False,
            "feedback": scenario['loss_feedback'],
            "amount": -scenario['loss_amount'] # Send the loss as a negative number
        }

    return jsonify(response)

# Run the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)