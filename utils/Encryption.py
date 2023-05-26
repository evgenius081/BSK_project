import base64
import os
import random
import hashlib

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from classes.CipherModes import *

BLOCK_SIZE = 16


class Encryption:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.session_key = None
        self.size_key = 2048
        self.key_file = f"private_key.pem"
        self.key_dir = "key/private"

    def create_private_key(self, key) -> None:
        num = random.randint(1, 300)
        self.key_file = f"privateKey_{num}.pem"
        print(key)
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)

        path = os.path.join(self.key_dir, self.key_file)
        if not os.path.exists(path):
            self.private_key = RSA.generate(self.size_key)
            self.create_public_key()
            with open(path, "wb") as file:
                file.write(AES.new(key, AES.MODE_CBC).encrypt(
                    pad(self.private_key.exportKey(), AES.block_size)))
                file.close()
        else:
            with open(path, "rb") as file:
                self.private_key = RSA.importKey(file.read())
                self.create_public_key()
                file.close()

    def create_public_key(self) -> bytes:
        self.public_key = self.private_key.publickey()
        return self.public_key

    def hash(self, value):
        return hashlib.sha256(bytes(value, "utf-8")).hexdigest()

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

    def encrypt_key(self, public_key, data) -> bytes:
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)

    def decrypt_key(self, private_key, data) -> bytes:
        decryptor = PKCS1_OAEP.new(private_key)
        return decryptor.decrypt(data)

