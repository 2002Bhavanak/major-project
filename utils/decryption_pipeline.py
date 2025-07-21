def decrypt_pipeline(stego_image_path, faculty_id):
    try:
        # Ensure extension is stripped from faculty_id for key lookup
        base_id = os.path.splitext(faculty_id)[0]
        key_path = os.path.join(KEY_FOLDER, f"{base_id}.key")
        if not os.path.exists(key_path):
            return False, f"Key file not found: {key_path}", None

        with open(key_path, "rb") as key_file:
            key = key_file.read()
        cipher = Fernet(key)

        # Extract ZIP and hash from the stego image
        extracted_zip_path, extracted_hash = extract_file_from_image(stego_image_path)

        if not extracted_zip_path:
            return False, "No embedded ZIP found in image.", None

        # Verify the hash of the extracted ZIP
        actual_hash = calculate_sha256(extracted_zip_path)
        if actual_hash != extracted_hash:
            return False, "Hash mismatch! File may have been tampered with.", None

        # Extract ZIP contents to a temporary folder
        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(extracted_zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)

            # Decrypt each file
            decrypted_files = []
            for filename in os.listdir(tmpdirname):
                file_path = os.path.join(tmpdirname, filename)
                with open(file_path, "rb") as enc_file:
                    encrypted_data = enc_file.read()
                decrypted_data = cipher.decrypt(encrypted_data)

                decrypted_file_path = os.path.join(DECRYPTED_FOLDER, filename.replace(".enc", ""))
                os.makedirs(os.path.dirname(decrypted_file_path), exist_ok=True)
                with open(decrypted_file_path, "wb") as dec_file:
                    dec_file.write(decrypted_data)
                decrypted_files.append(decrypted_file_path)

                # Convert if needed (e.g., audio to text, PDF to DOCX)
                convert_file_format(decrypted_file_path)

        return True, "Decryption successful.", decrypted_files

    except Exception as e:
        return False, f"Error during decryption: {str(e)}", None
