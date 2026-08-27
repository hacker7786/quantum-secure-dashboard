import os
import requests
from config import FABRIC_ENABLED, FABRIC_GATEWAY_URL
def log_to_blockchain(event_id: str, encrypted_event: str, timestamp: str) -> dict:
if not FABRIC_ENABLED:
return {
"status": "disabled",
"event_id": event_id,
}
payload = {
"event_id": event_id,
"encrypted_event": encrypted_event,
"timestamp": timestamp,
}
response = requests.post(
f"{FABRIC_GATEWAY_URL}/api/events",
json=payload,
timeout=5,
)
response.raise_for_status()
return response.json()
