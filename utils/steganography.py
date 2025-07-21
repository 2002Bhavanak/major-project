import cv2
import numpy as np
import os
import tempfile

# Utility to convert hash to bytes and back
def string_to_bytes(s):
    return s.encode('utf-8')

def bytes_to_string(b):
    return b.decode('utf-8')

def embed_file_in_image(zip_path, file_hash, cover_image_path, output_stego_path):
    # Logic here

    # Read the cover image
    image = cv2.imread(cover_image_path)
    if image is None:
        raise ValueError("Cover image not found or invalid.")

    # Read the zip file and append hash to end
    with open(zip_path, 'rb') as f:
        zip_data = f.read()
    combined_data = zip_data + b'||HASH||' + file_hash.encode()

    # Convert data to bits
    data_bits = ''.join(format(byte, '08b') for byte in combined_data)
    data_len = len(data_bits)

    # Check if image can hold the data
    height, width, _ = image.shape
    capacity = height * width * 3
    if data_len > capacity:
        raise ValueError("Cover image is too small to hold the data.")

    flat_image = image.flatten()

    for i in range(data_len):
        flat_image[i] = (flat_image[i] & ~1) | int(data_bits[i])

    encoded_image = flat_image.reshape(image.shape)

    output_path = os.path.join("stego_images", os.path.basename(zip_path).replace(".zip", "_stego.png"))
    cv2.imwrite(output_path, encoded_image)
    return output_path


def extract_file_from_image(stego_image_path):
    image = cv2.imread(stego_image_path)
    if image is None:
        raise ValueError("Stego image not found or invalid.")

    flat_image = image.flatten()

    bits = ''
    for byte in flat_image:
        bits += str(byte & 1)

    # Convert bits to bytes
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    data = bytearray()
    for byte_str in bytes_list:
        try:
            byte = int(byte_str, 2)
            data.append(byte)
        except:
            break

    # Split zip and hash
    marker = b'||HASH||'
    if marker not in data:
        return None, None

    zip_data, hash_data = data.split(marker, 1)

    # Save zip data to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
        tmp_zip.write(zip_data)
        zip_path = tmp_zip.name

    return zip_path, hash_data.decode(errors='ignore')
