from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import os
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            if allowed_file(file.filename):
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4()}.{file_ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                download_link = url_for('uploaded_file', filename=filename, _external=True)
                return render_template('success.html', link=download_link)
            else:
                flash('Nur PDF-Dateien sind erlaubt.')
                return redirect(request.url)

            file_ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{file_ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            download_link = url_for('uploaded_file', filename=filename, _external=True)
            return render_template('success.html', link=download_link)
    return render_template('index.html')

@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
