# Secure Question Paper Encryption System

A Flask-based web application for encrypting question papers using steganography and cryptographic techniques.

## Features

- **File Encryption**: Encrypt various file types (PDF, DOC, DOCX, MP3, WAV, ZIP, RAR)
- **Steganography**: Hide encrypted data in images using LSB (Least Significant Bit) technique
- **Key Management**: Generate and manage encryption keys for faculty members
- **Hash Verification**: Ensure file integrity with SHA-256 hashing
- **Web Interface**: User-friendly web interface for encryption operations

## Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start_server.sh
```

### Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Accessing the Application

The application runs on `http://0.0.0.0:5000` by default, which means:
- **Local access**: http://localhost:5000
- **Network access**: http://[YOUR_IP]:5000

## Common Issues and Solutions

### 1. "Site Not Reached" Error

**Causes and Solutions:**

- **Missing Dependencies**: Fixed by installing required packages in `requirements.txt`
- **Port Binding Issues**: The app now binds to `0.0.0.0:5000` for external access
- **Firewall/Network**: Ensure port 5000 is open if accessing from another machine

### 2. Import Errors

If you see `ModuleNotFoundError`, ensure you're running in the virtual environment:
```bash
source venv/bin/activate
python app.py
```

### 3. Permission Errors

Make the startup script executable:
```bash
chmod +x start_server.sh
```

### 4. File Upload Issues

Ensure these directories exist (automatically created by the startup script):
- `uploads/`
- `stego_images/`
- `keys/`
- `encrypted/`
- `hash/`
- `payload_zip/`

## Project Structure

```
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── start_server.sh          # Startup script
├── templates/
│   └── index.html           # Web interface
├── static/
│   └── covers/              # Cover images for steganography
├── utils/                   # Utility modules
│   ├── pipeline.py          # Main encryption pipeline
│   ├── stego_util.py        # Steganography utilities
│   ├── zip_util.py          # ZIP file utilities
│   └── ...                  # Other utility modules
└── [Generated Directories]
    ├── uploads/             # Uploaded files
    ├── stego_images/        # Generated steganographic images
    ├── keys/                # Encryption keys
    ├── encrypted/           # Encrypted files
    ├── hash/                # Hash files
    └── payload_zip/         # ZIP payloads
```

## How It Works

1. **Upload**: User uploads a file and enters Faculty ID
2. **Encryption**: File is encrypted using Fernet (AES 128)
3. **Hashing**: SHA-256 hash is calculated for integrity
4. **Packaging**: Encrypted file and hash are zipped together
5. **Steganography**: ZIP payload is embedded in a cover image using LSB
6. **Download**: User receives the steganographic image

## Dependencies

- **Flask 3.1.1**: Web framework
- **cryptography 45.0.5**: Encryption/decryption
- **Pillow 11.3.0**: Image processing
- **Werkzeug 3.1.3**: WSGI utilities

## Security Features

- **AES Encryption**: Industry-standard encryption
- **Key Management**: Unique keys per faculty member
- **Hash Verification**: Detect file tampering
- **Steganography**: Hide encrypted data in plain sight

## Development Status

- ✅ **Encryption**: Fully functional
- ✅ **Key Generation**: Working
- ✅ **Web Interface**: Complete
- 🚧 **Decryption**: Under development
- 🚧 **Format Conversion**: Planned feature

## Troubleshooting

If you encounter issues:

1. **Check the logs**: Flask runs in debug mode and shows detailed error messages
2. **Verify dependencies**: All packages in `requirements.txt` should be installed
3. **Check file permissions**: Ensure the application can read/write to all directories
4. **Network connectivity**: For external access, verify firewall settings

## Support

For issues related to:
- Missing dependencies → Use the provided `requirements.txt`
- Network access → Ensure the app binds to `0.0.0.0:5000`
- File operations → Check directory permissions and available disk space