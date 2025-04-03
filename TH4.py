import py_compile
import base64
import os
import tempfile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def convert_to_pyc(py_file):
    compiled = "temp_code.pyc"
    py_compile.compile(py_file, cfile=compiled)
    return compiled

def aes_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))

def create_loader_with_external_decryptor(pyc_file, output_file):
    with open(pyc_file, 'rb') as f:
        pyc_data = f.read()

    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    encrypted_data = aes_encrypt(pyc_data, key, iv)

    encoded_data = base64.b64encode(encrypted_data).decode()
    encoded_key = base64.b64encode(key).decode()
    encoded_iv = base64.b64encode(iv).decode()

    loader_code = f"""
import urllib.request, tempfile, importlib.util, base64

# تحميل دالة decrypt_and_run من GitHub
url = "https://raw.githubusercontent.com/waelhadi/TH1/main/secure_loader.py"
code = urllib.request.urlopen(url).read()

with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
    f.write(code)
    path = f.name

spec = importlib.util.spec_from_file_location("secure_loader", path)
secure_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(secure_loader)

# تمرير البيانات المشفرة للدالة
data_b64 = \"\"\"{encoded_data}\"\"\"
key_b64 = \"\"\"{encoded_key}\"\"\"
iv_b64  = \"\"\"{encoded_iv}\"\"\"

secure_loader.decrypt_and_run(data_b64, key_b64, iv_b64)
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(loader_code)

    os.remove(pyc_file)
    print(f"\nتم إنشاء الملف المشفر بنجاح: {output_file}")
    print("يتم تحميل دالة فك التشفير من GitHub عند التشغيل.")

# الاستخدام:
if __name__ == "__main__":
    py_file = input("أدخل اسم الملف الأصلي (مثال: tool.py): ").strip()
    out_file = input("اسم الملف المشفر الناتج (مثال: loader.py): ").strip()
    compiled_pyc = convert_to_pyc(py_file)
    create_loader_with_external_decryptor(compiled_pyc, out_file)
