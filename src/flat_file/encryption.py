from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64

KEY = get_random_bytes(32)  # AES-256

def encrypt(plaintext: str) -> str:
    data = plaintext.encode("utf-8")
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(iv + ciphertext).decode("utf-8")

def decrypt(encoded: str) -> str:
    raw = base64.b64decode(encoded)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    result = plaintext.decode("utf-8")
    plaintext = b'\x00' * len(plaintext)
    return result

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()