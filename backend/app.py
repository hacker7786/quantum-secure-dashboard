from flask import Flask, jsonify, request, send_from_directory
import json
import os
from datetime import datetime, timezone
from models.threat_detection_model import predict_threat
from models.quantum_encryption import encrypt_data
from utils.blockchain_utils import log_to_blockchain
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
@app.get("/")
def index():
return send_from_directory(FRONTEND_DIR, "index.html")
@app.get("/api/health")
def health():
return jsonify({"status": "ok", "service": "quantum-secure-dashboard"})
@app.post("/api/analyze")
def analyze():
body = request.get_json(silent=True) or {}
traffic = body.get("network_traffic")
if not isinstance(traffic, list) or not traffic:
return jsonify({"error": "network_traffic must be a non-empty list"}), 400
try:
result = predict_threat(traffic)
event = {
"event_id": result["event_id"],
"timestamp": datetime.now(timezone.utc).isoformat(),
"threat": result,
"network_traffic": traffic,
}
encrypted = encrypt_data(json.dumps(event, separators=(",", ":")))
blockchain_result = log_to_blockchain(
event_id=result["event_id"],
encrypted_event=encrypted["ciphertext"],
timestamp=event["timestamp"],
)
return jsonify({
"event_id": result["event_id"],
"timestamp": event["timestamp"],
"threat": result,
"encryption": {
"algorithm": encrypted["kem_algorithm"],
"symmetric_cipher": encrypted["symmetric_cipher"],
"ciphertext": encrypted["ciphertext"],
"kem_ciphertext": encrypted["kem_ciphertext"],
},
"blockchain": blockchain_result,
})
except Exception as exc:
app.logger.exception("analysis failed")
return jsonify({"error": "analysis failed", "detail": str(exc)}), 500
if __name__ == "__main__":
host = os.getenv("FLASK_HOST", "127.0.0.1")
port = int(os.getenv("FLASK_PORT", "5000"))
debug = os.getenv("FLASK_DEBUG", "0") == "1"
app.run(host=host, port=port, debug=debug)
