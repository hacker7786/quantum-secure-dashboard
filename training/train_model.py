from pathlib import Path
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "network_traffic.csv"
OUT = ROOT / "backend" / "trained" / "threat_model.joblib"
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
df = pd.read_csv(DATA)
X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = df["label"].astype(int)
preprocessor = ColumnTransformer([
("num", "passthrough", NUMERIC_FEATURES),
("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
])
pipeline = Pipeline([
("preprocessor", preprocessor),
("classifier", RandomForestClassifier(
n_estimators=200,
random_state=42,
class_weight="balanced",
)),
])
pipeline.fit(X, y)
OUT.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(pipeline, OUT)
print(f"saved model: {OUT}")
