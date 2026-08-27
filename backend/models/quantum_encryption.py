import base64
import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
# ML-KEM-768 is the NIST-standardized successor naming for Kyber-768.
# The KEM establishes a shared secret; AES-256-GCM encrypts the actual payload.
_private_key = mlkem.MLKEM768PrivateKey.generate()
_public_key = _private_key.public_key()
def _derive_aes_key(shared_secret: bytes) -> bytes:
return HKDF(
algorithm=hashes.SHA256(),
length=32,
salt=None,
info=b"quantum-secure-dashboard/aes-256-gcm",
).derive(shared_secret)
def encrypt_data(plaintext: str) -> dict:
shared_secret, kem_ciphertext = _public_key.encapsulate()
aes_key = _derive_aes_key(shared_secret)
nonce = os.urandom(12)
ciphertext = AESGCM(aes_key).encrypt(
nonce,
plaintext.encode("utf-8"),
associated_data=b"quantum-secure-dashboard",
)
return {
"kem_algorithm": "ML-KEM-768",
"symmetric_cipher": "AES-256-GCM",
"kem_ciphertext": base64.b64encode(kem_ciphertext).decode(),
"nonce": base64.b64encode(nonce).decode(),
"ciphertext": base64.b64encode(ciphertext).decode(),
}
def decrypt_data(envelope: dict) -> str:
kem_ciphertext = base64.b64decode(envelope["kem_ciphertext"])
nonce = base64.b64decode(envelope["nonce"])
ciphertext = base64.b64decode(envelope["ciphertext"])
shared_secret = _private_key.decapsulate(kem_ciphertext)
aes_key = _derive_aes_key(shared_secret)
plaintext = AESGCM(aes_key).decrypt(
nonce,
ciphertext,
associated_data=b"quantum-secure-dashboard",
)
return plaintext.decode("utf-8")
