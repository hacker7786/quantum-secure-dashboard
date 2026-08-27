backend/config.py
import os
MODEL_PATH = os.getenv(
"MODEL_PATH",
os.path.join(os.path.dirname(__file__), "trained", "threat_model.joblib"),
)
FABRIC_GATEWAY_URL = os.getenv(
"FABRIC_GATEWAY_URL",
"http://127.0.0.1:8080",
)
FABRIC_ENABLED = os.getenv("FABRIC_ENABLED", "1") == "1"
