# utils/hash_util.py

import hashlib

def compute_sha256(file_path):
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        hash_digest = hashlib.sha256(file_bytes).hexdigest()
    return hash_digest

def save_hash_to_file(hash_value, output_path):
    with open(output_path, "w") as f:
        f.write(hash_value)

def verify_sha256(file_path, expected_hash):
    actual_hash = compute_sha256(file_path)
    return actual_hash == expected_hash
