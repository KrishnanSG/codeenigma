import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE = os.urandom(12)  # randomly selected 96-bit nonce
SECRET_KEY = key = AESGCM.generate_key(bit_length=256)
