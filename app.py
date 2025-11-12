# ================================================================
# ⚙️ GOD FORGE — MAIN FLASK APP
# ================================================================

from flask import Flask, render_template, request, jsonify
import json, os, uuid, socket

app = Flask(__name__)

# ================================================================
# 🗄 FILE PATHS
# ================================================================
HEROES_FILE = "heroes.json"
PROGRESSION_FILE = "progression.json"

# ================================================================
# 🧩 HELPER FUNCTIONS
# ================================================================
def load_json(file, default):
    """Load JSON data or return default if file missing."""
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    """Save data as JSON with indentation."""
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ================================================================
# 🦸 HEROES API
# ================================================================
@app.route("/heroes")
def get_heroes():
    """Return list of all heroes as JSON."""
    return jsonify(load_json(HEROES_FILE, []))

@app.route("/add", methods=["POST"])
def add_hero():
    """Add a new hero entry."""
    heroes = load_json(HEROES_FILE, [])
    new_hero = {
        "id": str(uuid.uuid4()),
        "name": "",
        "level": "",
        "power": ""
    }
    heroes.append(new_hero)
    save_json(HEROES_FILE, heroes)
    return jsonify(new_hero)

@app.route("/update", methods=["POST"])
def update_hero():
    """Update a specific hero field (name, level, power)."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="Invalid JSON"), 400

    heroes = load_json(HEROES_FILE, [])
    for hero in heroes:
        if hero["id"] == data.get("id"):
            if data["field"] in {"name", "level", "power"}:
                hero[data["field"]] = data["value"]

    save_json(HEROES_FILE, heroes)
    return jsonify(success=True)

@app.route("/delete", methods=["POST"])
def delete_hero():
    """Delete a hero by ID."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="Invalid JSON"), 400

    heroes = load_json(HEROES_FILE, [])
    updated = [h for h in heroes if h["id"] != data.get("id")]
    save_json(HEROES_FILE, updated)
    return jsonify(success=True)

# ================================================================
# 🧭 PROGRESSION API
# ================================================================
@app.route("/progression")
def get_progression():
    """Return progression stats JSON."""
    return jsonify(load_json(PROGRESSION_FILE, {
        "wins": 0,
        "losses": 0,
        "stages_cleared": 0,
        "achievements": []
    }))

@app.route("/progression/update", methods=["POST"])
def update_progression():
    """Update player progression fields."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="Invalid JSON"), 400

    progression = load_json(PROGRESSION_FILE, {
        "wins": 0,
        "losses": 0,
        "stages_cleared": 0,
        "achievements": []
    })

    for key in ["wins", "losses", "stages_cleared", "achievements"]:
        if key in data:
            progression[key] = data[key]

    save_json(PROGRESSION_FILE, progression)
    return jsonify(success=True)

@app.route("/progression/reset", methods=["POST"])
def reset_progression():
    """Reset progression stats."""
    progression = {
        "wins": 0,
        "losses": 0,
        "stages_cleared": 0,
        "achievements": []
    }
    save_json(PROGRESSION_FILE, progression)
    return jsonify(success=True, progression=progression)

# ================================================================
# 🖥 FRONTEND ROUTES (Tabs + Pages)
# ================================================================

@app.route("/")
def home():
    """Render Home page (main God Forge screen)."""
    return render_template("home.html", active_tab="home")

@app.route("/hero")
def hero():
    """Render Hero tab — blank background for now."""
    return render_template("hero.html", active_tab="hero")

@app.route("/settings")
def settings():
    """Render Settings tab."""
    return render_template("settings.html", active_tab="settings")

# ================================================================
# 🗂 CARD PAGES
# ================================================================
@app.route("/card1")
def card1():
    return render_template("card1.html", title="Help Links")

@app.route("/card2")
def card2():
    return render_template("card2.html", title="Card Two")

@app.route("/card3")
def card3():
    return render_template("card3.html", title="Card Three")

# ================================================================
# 🔍 PORT FINDER
# ================================================================
def find_free_port(start_port=5000, max_port=5100):
    """Find first available port between start_port and max_port."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError("No free ports available in range 5000–5100")

# ================================================================
# 🚀 APP LAUNCHER
# ================================================================
if __name__ == "__main__":
    port = find_free_port()
    print(f"✅ Starting God Forge Flask app on port {port}")
    app.run(debug=True, port=port)
