# Quantum-Secure Cyber Security Dashboard
## Overview
A portfolio-oriented SOC dashboard that demonstrates:
- ML-based network threat classification
- Post-quantum key encapsulation using ML-KEM-768
- AES-256-GCM authenticated encryption
- Hyperledger Fabric audit logging through a Gateway adapter
- Flask API
- HTML/CSS/JavaScript dashboard
- Docker-based deployment
## Important terminology
The original design called the algorithm "CRYSTALS-Kyber". Kyber is the research/algorithm family; the NIST standardized KEM is ML-KEM
The cryptographic flow is:
ML-KEM-768 -> shared secret -> HKDF-SHA256 -> AES-256-GCM -> encrypted event
ML-KEM is a KEM, not a bulk-encryption algorithm.
## 1. Local Python setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Train the model once:
```bash
python training/train_model.py
```
Run Flask:
```bash
python backend/app.py
```
Open:
http://127.0.0.1:5000
## 2. Test the API
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
-H 'Content-Type: application/json' \
-d '{
"network_traffic": [{
"src_ip": "10.10.10.21",
"dst_ip": "10.10.10.5",
"packet_size": 64,
"duration_ms": 300,
"src_port": 49153,
"dst_port": 22,
"protocol": "TCP",
"bytes_sent": 600,
"bytes_received": 120,
"failed_connections": 8,
"connection_count": 25
}]
}'
```
## 3. Hyperledger Fabric
Do not run a standalone `hyperledger/fabric-peer` container and call it a blockchain API.
Use the official Fabric samples test network:
```bash
git clone https://github.com/hyperledger/fabric-samples.git
cd fabric-samples/test-network
./network.sh up createChannel
```
Then deploy a security-audit chaincode/smart contract that exposes a transaction such as:
```text
CreateEvent(eventId, encryptedEvent, timestamp)
ReadEvent(eventId)
```
The Flask service should call a Fabric Gateway adapter. The adapter should use the certificates and identities created by the Fabric te
After the real Fabric Gateway is configured, set:
```bash
export FABRIC_ENABLED=1
export FABRIC_GATEWAY_URL=http://127.0.0.1:8080
```
## 4. Docker
```bash
docker compose build
docker compose up
```
The supplied compose file intentionally does not pretend that a peer container alone is a complete Fabric network. Configure the Fabric
## Security notes
This is a learning/portfolio system, not a production SOC.
Before production use:
- TLS everywhere
- authentication and authorization
- secret/key management
- key rotation
- persistent key storage/HSM where appropriate
- input size limits
- rate limiting
- CSRF/CORS policy as appropriate
- secure model artifact provenance
- dataset validation
- audit integrity monitoring
- SIEM integration
- real Fabric identity management
- monitoring and alerting
The demo crypto module generates a process-local ML-KEM key. Production systems must use managed/persistent keys and define a secure ke
## Recommended SOC extensions
- MITRE ATT&CK technique mapping
- IOC extraction
- Sigma-rule correlation
- PCAP ingestion
- Zeek/Suricata integration
- authentication and RBAC
- alert acknowledgement workflow
- analyst notes
- threat-intelligence enrichment
- Grafana/Prometheus metrics
- WebSocket live alerts
