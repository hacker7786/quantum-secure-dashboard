import os
import uuid
import joblib
import pandas as pd
MODEL_PATH = os.getenv(
"MODEL_PATH",
os.path.join(os.path.dirname(__file__), "..", "trained", "threat_model.joblib"),
)
NUMERIC_FEATURES = [
"packet_size",
"duration_ms",
"src_port",
"dst_port",
"bytes_sent",
"bytes_received",
"failed_connections",
"connection_count",
]
CATEGORICAL_FEATURES = ["protocol"]
def _validate_traffic(traffic):
if not isinstance(traffic, list) or not traffic:
raise ValueError("traffic must be a non-empty list")
required = set(NUMERIC_FEATURES + CATEGORICAL_FEATURES)
for row in traffic:
missing = required - set(row.keys())
if missing:
raise ValueError(f"missing fields: {sorted(missing)}")
def predict_threat(traffic):
_validate_traffic(traffic)
if not os.path.exists(MODEL_PATH):
raise FileNotFoundError(
f"trained model not found at {MODEL_PATH}. Run training/train_model.py first."
)
model = joblib.load(MODEL_PATH)
df = pd.DataFrame(traffic)
X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
probabilities = model.predict_proba(X)
predictions = model.predict(X)
# Mean malicious probability across observed flows.
classes = list(model.classes_)
malicious_index = classes.index(1) if 1 in classes else None
if malicious_index is not None:
risk = float(probabilities[:, malicious_index].mean())
else:
risk = float((predictions == 1).mean())
if risk >= 0.80:
severity = "CRITICAL"
elif risk >= 0.60:
severity = "HIGH"
elif risk >= 0.30:
severity = "MEDIUM"
else:
severity = "LOW"
confidence = float(probabilities.max(axis=1).mean())
return {
"event_id": str(uuid.uuid4()),
"severity": severity,
"risk_score": round(risk * 100, 2),
"confidence": round(confidence * 100, 2),
"malicious_flows": int((predictions == 1).sum()),
"total_flows": int(len(predictions)),
}
