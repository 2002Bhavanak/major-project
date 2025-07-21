from PIL import Image
import zipfile
import os

# Create a ZIP file containing the encrypted file and the hash file
def create_payload_zip(encrypted_path, hash_path, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        zipf.write(encrypted_path, arcname=os.path.basename(encrypted_path))
        zipf.write(hash_path, arcname=os.path.basename(hash_path))

# Embed the contents of the ZIP payload file into the cover image using LSB steganography
def embed_file_in_image(cover_image_path, payload_zip_path, output_image_path):
    img = Image.open(cover_image_path)
    img = img.convert('RGB')

    # Read payload ZIP file as bytes
    with open(payload_zip_path, 'rb') as f:
        payload_bytes = f.read()

    # Convert payload bytes into a binary string
    payload_bits = ''.join(f'{byte:08b}' for byte in payload_bytes)
    payload_len = len(payload_bits)

    pixels = list(img.getdata())
    new_pixels = []

    bit_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if bit_index < payload_len:
            r = (r & ~1) | int(payload_bits[bit_index])
            bit_index += 1
        if bit_index < payload_len:
            g = (g & ~1) | int(payload_bits[bit_index])
            bit_index += 1
        if bit_index < payload_len:
            b = (b & ~1) | int(payload_bits[bit_index])
            bit_index += 1
        new_pixels.append((r, g, b))

    if bit_index < payload_len:
        raise ValueError("Cover image not large enough to hold payload!")

    # Create and save the stego image
    stego_img = Image.new(img.mode, img.size)
    stego_img.putdata(new_pixels)
    stego_img.save(output_image_path)

    return output_image_path  # ✅ IMPORTANT: Return the output path

# Extract the embedded ZIP payload from a stego image
def extract_data_from_image(stego_image_path, output_zip_path, payload_size):
    img = Image.open(stego_image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())

    bits = ""
    for pixel in pixels:
        for channel in pixel[:3]:  # Use R, G, B channels
            bits += str(channel & 1)

    # Convert binary string to bytes
    payload_bytes = bytearray()
    for i in range(0, payload_size * 8, 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            payload_bytes.append(int(byte, 2))

    with open(output_zip_path, 'wb') as f:
        f.write(payload_bytes)
        
