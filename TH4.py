import base64
import tempfile
import runpy
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_and_run(data_b64, key_b64, iv_b64):
    data = base64.b64decode(data_b64)
    key = base64.b64decode(key_b64)
    iv = base64.b64decode(iv_b64)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(data), AES.block_size)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pyc") as f:
        f.write(decrypted)
        path = f.name

    runpy.run_path(path)
    os.unlink(path)
