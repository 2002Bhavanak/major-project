# utils/crypto_util.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from cryptography.fernet import Fernet
import os

BLOCK_SIZE = 16  # AES block size

def generate_key():
    return get_random_bytes(32)  # AES-256

def encrypt_file(input_path, output_path, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(input_path, 'rb') as f_in:
        data = f_in.read()

    ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE))

    with open(output_path, 'wb') as f_out:
        f_out.write(iv + ciphertext)  # prepend IV for later decryption

def decrypt_file(encrypted_path, output_path, key):
    with open(encrypted_path, 'rb') as f_in:
        iv = f_in.read(16)
        ciphertext = f_in.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)

    with open(output_path, 'wb') as f_out:
        f_out.write(plaintext)

import hashlib

def calculate_sha256(file_path):
    """Calculates SHA-256 hash of the given file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
