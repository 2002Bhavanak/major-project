import zipfile
import os

def create_payload_zip(encrypted_file_path, hash_file_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        zipf.write(encrypted_file_path, arcname=os.path.basename(encrypted_file_path))
        zipf.write(hash_file_path, arcname=os.path.basename(hash_file_path))
