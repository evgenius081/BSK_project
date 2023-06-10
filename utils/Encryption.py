import base64
import os
import random
import hashlib

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from timeit import default_timer as timer

BLOCK_SIZE = 16


class Encryption:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.session_key = None
        self.size_key = 2048
        self.key_file = f"private_key.pem"
        self.key_dir = "key/private"
        self.chat = None

    def create_private_key(self, key) -> None:
        num = random.randint(1, 300)
        self.key_file = f"privateKey_{num}.pem"
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)

        path = os.path.join(self.key_dir, self.key_file)
        self.private_key = RSA.generate(self.size_key)
        self.create_public_key()
        with open(path, "wb") as file:
            iv = get_random_bytes(BLOCK_SIZE)
            file.write(AES.new(key, AES.MODE_CBC, iv).encrypt(
                pad(self.private_key.exportKey(), BLOCK_SIZE)))
            file.close()

    def create_public_key(self) -> bytes:
        self.public_key = self.private_key.publickey()
        return self.public_key

    def hash(self, value) -> bytes:
        return hashlib.sha256(bytes(value, "utf-8")).digest()

    def generate_session_key(self) -> bytes:
        self.session_key = get_random_bytes(BLOCK_SIZE)
        return self.session_key

    def encrypt_mode(self, raw: bytes, mode=AES.MODE_ECB) -> bytes:
        key = self.session_key
        if mode == AES.MODE_CBC:
            iv = get_random_bytes(BLOCK_SIZE)
        raw = pad(raw.encode(), BLOCK_SIZE)

        if mode == AES.MODE_ECB:
            cipher = AES.new(key, mode)
            return base64.b64encode(cipher.encrypt(raw))
        if mode == AES.MODE_CBC:
            cipher = AES.new(key, mode, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt_mode(self, enc, mode=AES.MODE_ECB) -> bytes:
        key = self.session_key
        enc = base64.b64decode(enc + b'=' * (-len(enc) % 4))

        if mode == AES.MODE_ECB:
            cipher = AES.new(key, mode)
            return unpad(cipher.decrypt(enc), BLOCK_SIZE)
        if mode == AES.MODE_CBC:
            cipher = AES.new(key, mode, enc[:BLOCK_SIZE])
            return unpad(cipher.decrypt(enc[BLOCK_SIZE:]), BLOCK_SIZE)

    def encrypt_file(self, in_file, file_message, out_file=None, mode=AES.MODE_ECB, chunk_size=1024 * 1024) -> str:
        key = self.session_key

        if not out_file:
            out_file = in_file + '.enc'

        if mode == AES.MODE_ECB:
            cipher = AES.new(key, mode)
        else:
            iv = get_random_bytes(BLOCK_SIZE)
            cipher = AES.new(key, mode, iv)

        with open(in_file, 'rb') as infile:
            with open(out_file, 'wb') as outfile:
                if mode is not AES.MODE_ECB:
                    outfile.write(iv)

                in_file_size = os.path.getsize(in_file)
                counter = 0
                file_message.set_encrypting()
                while True:
                    chunk = infile.read(chunk_size)
                    counter += chunk_size
                    file_message.update_procent(int(counter/in_file_size * 100))
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode("utf-8")

                    outfile.write(cipher.encrypt(chunk))
        return out_file

    def decrypt_file(self, in_file, size, file_message, out_file=None, mode=AES.MODE_ECB, chunk_size=1024 * 1024) -> str:
        start_timer = timer()
        key = self.session_key
        if not out_file:
            out_file = os.path.splitext(in_file)[0]

        with open(in_file, 'rb') as infile:
            original_size = size
            counter = 0

            if mode == AES.MODE_ECB:
                cipher = AES.new(key, mode)
            else:
                iv = infile.read(16)
                original_size -= 16
                cipher = AES.new(key, mode, iv)

            with open(out_file, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunk_size)
                    counter += chunk_size
                    file_message.update_procent(int(counter / original_size * 100))
                    if len(chunk) == 0:
                        break
                    cip = cipher.decrypt(chunk)
                    outfile.write(cip)

                outfile.truncate(original_size)

        end_timer = timer()
        print("Decrypting file time is", end_timer - start_timer)
        return out_file

    def encrypt_key(self, public_key, data) -> bytes:
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)

    def decrypt_key(self, private_key, data) -> bytes:
        decryptor = PKCS1_OAEP.new(private_key)
        return decryptor.decrypt(data)

