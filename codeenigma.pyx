import base64
import marshal
import zlib
import types

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE = b"<randomly selected 96-bit nonce>"
SECRET_KEY = b"<key used for AES encryption>"

def execute_secure_code(secure_code: bytes, globals_dict=None) -> bytes:
    """Deobfuscate a single Python file."""

    if globals_dict is None:
        globals_dict = globals()

    # Decrypt the obfuscated code
    aesgcm = AESGCM(SECRET_KEY)
    decrypted = aesgcm.decrypt(NONCE, secure_code, associated_data=None)

    # Decode and decompress
    compressed = base64.b64decode(decrypted)
    marshaled = zlib.decompress(compressed)

    # Unmarshal to get the code object
    code_obj = marshal.loads(marshaled)

    if isinstance(code_obj, types.CodeType):
        exec(code_obj, globals_dict)
    else:
        raise ValueError("Invalid code object in obfuscated module")

