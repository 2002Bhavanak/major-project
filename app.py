from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from werkzeug.utils import secure_filename
from utils.pipeline import encrypt_pipeline

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'mp3', 'wav', 'zip', 'rar'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'input_file' not in request.files or not request.form.get('faculty_id'):
        flash('Please provide both Faculty ID and input file.')
        return redirect(url_for('index'))

    input_file = request.files['input_file']
    faculty_id = request.form.get('faculty_id').strip()

    if input_file and allowed_file(input_file.filename):
        filename = secure_filename(input_file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        input_file.save(input_path)

        # Use predefined cover image
        cover_image_path = os.path.join('static', 'covers', 'large_cover.png')

        # Set output stego image path
        stego_filename = f"{os.path.splitext(filename)[0]}_stego.png"
        stego_image_path = os.path.join('stego_images', stego_filename)
        os.makedirs('stego_images', exist_ok=True)

        success, message, result_path = encrypt_pipeline(input_path, cover_image_path, stego_image_path)

        if success and result_path and os.path.exists(result_path):
            flash(message)
            return send_file(result_path, as_attachment=True)
        else:
            flash("Encryption failed or stego image not found.")
            return redirect(url_for('index'))
    else:
        flash('Invalid file type.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

