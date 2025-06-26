
import base64
import marshal
import zlib
import types

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE = b'\x8c\xf0%67.pg\xd7UTo'
SECRET_KEY = b"\xeb\xcf\x83\xa9k\xf3.\xca\x93\xe0\xd3\x04\xbfp\xd0%'L\xe3\xd4\x83\xbb-\xf6\xa4\x03\x07\x1eY\xad\x96h"

def execute_secure_code(secure_code: bytes, globals_dict=None) -> bytes:

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
