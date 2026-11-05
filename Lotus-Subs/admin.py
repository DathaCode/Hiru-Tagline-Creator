"""
Admin lock for Settings, and at-rest protection for the Gemini API key.

- Settings opens only after the admin password is entered. Only a salted
  PBKDF2-SHA256 hash of the password is stored here. To change the password,
  run `python admin.py` and paste its output over the three constants below.
- The API key is saved encrypted with Windows DPAPI (bound to the Windows user
  account), so it is not readable as plain text in the registry.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets

PASSWORD_SALT = "9d370c7fbdeb1cf9bfad2d32af86906a"
PASSWORD_ITERATIONS = 310000
PASSWORD_HASH = "18d92aeeb3c0d82cd8499c5217cbaf9f784c1020cb0186df3b39f1fdb572d2db"


def _hash(password: str, salt: str, iterations: int) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), iterations).hex()


def check_password(password: str) -> bool:
    return hmac.compare_digest(_hash(password, PASSWORD_SALT, PASSWORD_ITERATIONS), PASSWORD_HASH)


# ------------------------------------------------------------ DPAPI ----------

_PREFIX = "dpapi:"


def _dpapi(data: bytes, protect: bool) -> bytes:
    import ctypes
    from ctypes import wintypes

    class Blob(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    buf = ctypes.create_string_buffer(data, len(data))
    blob_in, blob_out = Blob(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))), Blob()
    entropy = b"LotusSubs.api_key"
    ent_buf = ctypes.create_string_buffer(entropy, len(entropy))
    blob_ent = Blob(len(entropy), ctypes.cast(ent_buf, ctypes.POINTER(ctypes.c_char)))
    fn = ctypes.windll.crypt32.CryptProtectData if protect else ctypes.windll.crypt32.CryptUnprotectData
    args = ((ctypes.byref(blob_in), "LotusSubs") if protect else (ctypes.byref(blob_in), None))
    CRYPTPROTECT_UI_FORBIDDEN = 0x01
    if not fn(*args, ctypes.byref(blob_ent), None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(blob_out)):
        raise OSError("Windows could not encrypt/decrypt the API key.")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)


def protect(secret: str) -> str:
    if not secret:
        return ""
    if os.name != "nt":
        return secret
    return _PREFIX + base64.b64encode(_dpapi(secret.encode("utf-8"), True)).decode("ascii")


def unprotect(stored: str) -> str:
    """Decrypts a protected value; a plain (legacy) value is returned unchanged."""
    if not stored or not stored.startswith(_PREFIX):
        return stored or ""
    try:
        return _dpapi(base64.b64decode(stored[len(_PREFIX):]), False).decode("utf-8")
    except (OSError, ValueError):
        return ""  # saved by another Windows user or PC: the admin must enter it again


if __name__ == "__main__":
    import getpass
    pw = getpass.getpass("New admin password: ")
    if pw != getpass.getpass("Repeat it: "):
        raise SystemExit("The passwords don't match.")
    salt = secrets.token_hex(16)
    print(f'PASSWORD_SALT = "{salt}"')
    print(f"PASSWORD_ITERATIONS = {PASSWORD_ITERATIONS}")
    print(f'PASSWORD_HASH = "{_hash(pw, salt, PASSWORD_ITERATIONS)}"')
