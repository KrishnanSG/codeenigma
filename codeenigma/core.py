import base64
import marshal
import zlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from codeenigma.private import NONCE, SECRET_KEY


def obfuscate_file(file_path: str) -> bytes:
    """Obfuscate a single Python file."""
    with open(file_path, encoding="utf-8") as f:
        code = f.read()

    # Compile the code to a code object
    code_obj = compile(code, str(file_path), "exec")

    # Marshal the code object to bytes
    marshaled = marshal.dumps(code_obj)

    # Compress and encode
    compressed = zlib.compress(marshaled)
    obfuscated = base64.b64encode(compressed)

    # Encrypt the obfuscated code
    aesgcm = AESGCM(SECRET_KEY)

    ciphertext = aesgcm.encrypt(NONCE, obfuscated, associated_data=None)
    return ciphertext
