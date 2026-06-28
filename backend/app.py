from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Fetch all waste logs, newest first."""
    try:
        response = supabase.table("waste_logs").select("*").order("created_at", desc=True).execute()
        return jsonify({"success": True, "data": response.data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/logs", methods=["POST"])
def create_log():
    """Create a new waste log entry."""
    try:
        body = request.get_json()

        # Validate required fields
        required = ["category", "weight_kg", "latitude", "longitude"]
        for field in required:
            if field not in body or body[field] is None:
                return jsonify({"success": False, "error": f"Missing field: {field}"}), 400

        weight = float(body["weight_kg"])
        if weight <= 0:
            return jsonify({"success": False, "error": "Weight must be greater than 0"}), 400

        lat = float(body["latitude"])
        lng = float(body["longitude"])
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({"success": False, "error": "Invalid coordinates"}), 400

        record = {
            "category": body["category"],
            "weight_kg": weight,
            "latitude": lat,
            "longitude": lng,
            "notes": body.get("notes", ""),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        response = supabase.table("waste_logs").insert(record).execute()
        return jsonify({"success": True, "data": response.data[0]}), 201

    except ValueError:
        return jsonify({"success": False, "error": "Invalid numeric value"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return aggregated stats per waste category."""
    try:
        response = supabase.table("waste_logs").select("category, weight_kg").execute()
        data = response.data

        totals = {}
        grand_total = 0.0
        for row in data:
            cat = row["category"]
            w = float(row["weight_kg"])
            totals[cat] = round(totals.get(cat, 0.0) + w, 2)
            grand_total += w

        return jsonify({
            "success": True,
            "totals_by_category": totals,
            "grand_total_kg": round(grand_total, 2),
            "total_entries": len(data)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "EcoAudit API is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)