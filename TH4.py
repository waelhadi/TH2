import base64
import tempfile
import importlib.util
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_and_run(data_b64: str, aes_key: bytes, iv: bytes, xor_key: bytes, mode: str, repeat_count: int = 1):
    data = base64.b64decode(data_b64)

    for _ in range(repeat_count):
        if mode == "AES_XOR":
            data = xor_decrypt(data, xor_key)
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            data = unpad(cipher.decrypt(data), AES.block_size)
        elif mode == "XOR_AES":
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            data = unpad(cipher.decrypt(data), AES.block_size)
            data = xor_decrypt(data, xor_key)

    # حفظ الملف وتشغيله كـ .pyc
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pyc") as f:
        f.write(data)
        temp_path = f.name

    spec = importlib.util.spec_from_file_location("x", temp_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # يمكنك حذف الملف بعد التشغيل:
    # os.unlink(temp_path)
