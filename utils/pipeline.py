
import os
from cryptography.fernet import Fernet
import hashlib
from utils.zip_util import create_payload_zip
from utils.stego_util import embed_file_in_image

# Define folders
KEY_FOLDER = 'keys'
ENCRYPTED_FOLDER = 'encrypted'
HASH_FOLDER = 'hash'
ZIP_FOLDER = 'payload_zip'

# Create folders if they don't exist
for folder in [KEY_FOLDER, ENCRYPTED_FOLDER, HASH_FOLDER, ZIP_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def encrypt_pipeline(input_path, cover_image_path, output_stego_path):
    print("Starting encryption pipeline...")
    print("Input path:", input_path)
    print("Cover image path:", cover_image_path)

    # Generate key
    key = Fernet.generate_key()
    key_filename = os.path.basename(input_path) + ".key"
    key_path = os.path.join(KEY_FOLDER, key_filename)
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print("Key saved at:", key_path)

    # Encrypt the input file
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, os.path.basename(input_path) + ".enc")
    fernet = Fernet(key)
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted_data = fernet.encrypt(data)
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        print("File encrypted at:", encrypted_path)
    except Exception as e:
        print("Encryption failed:", e)
        return False, f"Encryption failed: {e}", None

    # Calculate hash
    hash_path = os.path.join(HASH_FOLDER, os.path.basename(input_path) + ".sha256")
    try:
        sha256_hash = hashlib.sha256(encrypted_data).hexdigest()
        with open(hash_path, 'w') as f:
            f.write(sha256_hash)
        print("Hash written at:", hash_path)
    except Exception as e:
        print("Hashing failed:", e)
        return False, f"Hashing failed: {e}", None

    # Zip payload
    payload_zip_path = os.path.join(ZIP_FOLDER, os.path.basename(input_path) + ".zip")
    try:
        create_payload_zip(encrypted_path, hash_path, payload_zip_path)
        print("Payload zipped at:", payload_zip_path)
    except Exception as e:
        print("Zipping failed:", e)
        return False, f"Zipping failed: {e}", None

    # Embed into image
    try:
        print("Embedding into image...")
        result_path = embed_file_in_image(cover_image_path, payload_zip_path, output_stego_path)
        print("Stego image saved at:", result_path)
        return True, "Encryption and embedding successful.", result_path
    except Exception as e:
        print("Embedding failed:", e)
        return False, f"Embedding failed: {e}", None
