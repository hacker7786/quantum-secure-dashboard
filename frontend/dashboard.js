const sampleTraffic = [
{
src_ip: "10.10.10.21",
dst_ip: "10.10.10.5",
packet_size: 1400,
duration_ms: 1200,
src_port: 49152,
dst_port: 443,
protocol: "TCP",
bytes_sent: 12000,
bytes_received: 45000,
failed_connections: 0,
connection_count: 4
},
{
src_ip: "10.10.10.21",
dst_ip: "10.10.10.5",
packet_size: 64,
duration_ms: 300,
src_port: 49153,
dst_port: 22,
protocol: "TCP",
bytes_sent: 600,
bytes_received: 120,
failed_connections: 8,
connection_count: 25
}
];
async function analyze() {
const output = document.getElementById("output");
output.textContent = "Analyzing...";
try {
const response = await fetch("/api/analyze", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({network_traffic: sampleTraffic})
});
const data = await response.json();
if (!response.ok) throw new Error(data.detail || data.error || "Request failed");
document.getElementById("severity").textContent = data.threat.severity;
document.getElementById("risk").textContent = `${data.threat.risk_score}%`;
document.getElementById("confidence").textContent = `${data.threat.confidence}%`;
document.getElementById("fabric").textContent = data.blockchain.status || "UNKNOWN";
output.textContent = JSON.stringify(data, null, 2);
} catch (error) {
output.textContent = `Error: ${error.message}`;
}
}
document.getElementById("analyze").addEventListener("click", analyze);
