from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def xor_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decrypt_and_run(data_b64, aes_key, aes_iv, xor_key, mode):
    try:
        encrypted = base64.b64decode(data_b64)

        if mode == "AES_XOR":
            decrypted = xor_decrypt(encrypted, xor_key)
            plain = AES.new(aes_key, AES.MODE_CBC, aes_iv).decrypt(decrypted)
            pyc_data = unpad(plain, AES.block_size)

        elif mode == "XOR_AES":
            aes_dec = AES.new(aes_key, AES.MODE_CBC, aes_iv).decrypt(encrypted)
            plain = xor_decrypt(unpad(aes_dec, AES.block_size), xor_key)
            pyc_data = plain

        else:
            print("وضع غير مدعوم:", mode)
            return

        import tempfile, importlib.util, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pyc") as f:
            f.write(pyc_data)
            temp_pyc = f.name

        spec = importlib.util.spec_from_file_location("x", temp_pyc)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        os.unlink(temp_pyc)

    except Exception as e:
        print("فشل فك التشفير:", e)
