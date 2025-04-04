from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_and_run(data_b64, aes_key, aes_iv, xor_key):
    try:
        encrypted = base64.b64decode(data_b64)
        decrypted_once = xor_decrypt(encrypted, xor_key)
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        pyc_data = unpad(cipher.decrypt(decrypted_once), AES.block_size)

        # حفظ وتشغيل ملف pyc مؤقت
        import tempfile, importlib.util, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pyc") as f:
            f.write(pyc_data)
            temp_pyc = f.name

        spec = importlib.util.spec_from_file_location("decrypted_module", temp_pyc)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        os.unlink(temp_pyc)
    except Exception as e:
        print("فشل فك التشفير:", e)
