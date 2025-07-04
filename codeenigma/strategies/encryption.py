import base64
import marshal
import zlib
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from codeenigma.strategies.base import BaseObfuscationStrategy


class CodeEnigmaObfuscationStrategy(BaseObfuscationStrategy):
    """
    Obfuscation strategy using AES-GCM encryption.
    """

    def __init__(self, secret_key: bytes, nonce: bytes):
        self.secret_key = secret_key
        self.nonce = nonce
        self.aesgcm = AESGCM(secret_key)

    @property
    def template_path(self) -> Path:
        return Path(__file__).parent / "encryption_runtime.py.template"

    @property
    def template_vars(self) -> dict:
        return {
            "nonce": repr(self.nonce),
            "secret_key": repr(self.secret_key),
        }

    def obfuscate(self, file_path: str, **kwargs) -> bytes:
        """
        Obfuscate the given Python code using AES-GCM encryption.

        Args:
            file_path: File path to the source code to obfuscate
            **kwargs: Additional arguments (not used)

        Returns:
            The obfuscated code wrapped in a secure execution environment
        """
        with open(file_path, encoding="utf-8") as f:
            code = f.read()

        # Compile the code to a code object
        code_obj = compile(code, str(file_path), "exec")

        # Marshal the code object to bytes
        marshaled = marshal.dumps(code_obj)

        # Compress and encode
        compressed = zlib.compress(marshaled)

        # Encode to base64
        obfuscated = base64.b64encode(compressed)

        # Encrypt the obfuscated code
        return self.aesgcm.encrypt(self.nonce, obfuscated, associated_data=None)
