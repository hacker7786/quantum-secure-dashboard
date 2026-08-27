// Production note:
// This service should use @hyperledger/fabric-gateway and the
// cryptographic identity/TLS material from a running Fabric test network.
//
// The endpoint below is a deliberately explicit integration boundary.
// It returns 503 until a real Fabric Gateway client is configured.
// Do not label a mock endpoint as a blockchain.
const express = require("express");
const app = express();
app.use(express.json({limit: "2mb"}));
app.post("/api/events", async (req, res) => {
const { event_id, encrypted_event, timestamp } = req.body;
if (!event_id || !encrypted_event || !timestamp) {
return res.status(400).json({status: "error", message: "missing fields"});
}
// Replace this section with a real Fabric Gateway transaction:
//
// const network = gateway.getNetwork("mychannel");
// const contract = network.getContract("security-audit");
// await contract.submitTransaction(
//
"CreateEvent", event_id, encrypted_event, timestamp
// );
//
// The official Fabric workflow requires a deployed chaincode/smart
// contract and a channel. See README for the test-network steps.
return res.status(503).json({
status: "fabric_not_configured",
event_id,
message: "Configure a real Fabric Gateway and deployed chaincode."
});
});
app.listen(8080, "0.0.0.0", () => {
console.log("Fabric gateway adapter listening on :8080");
});
