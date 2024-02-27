from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash
from flask_wtf import FlaskForm 
from wtforms import FileField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder='template')
app.config["UPLOAD_FOLDER"] = 'static/upload'
app.config["SECRET_KEY"] = "MYKEY"

class UploadForm(FlaskForm):
    file = FileField('File')

clipboard = ""

@app.route('/', methods=['GET', 'POST'])
def clipcopy():
    global clipboard
    if request.method == 'POST':
        clipboard = request.form['clipboard']
    form = UploadForm()
    return render_template('clipboard.html', clipboard=clipboard, form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash("File uploaded successfully", "success")
       
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', form=form, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("File deleted successfully", "success")
    else:
        flash("File not found", "error")
    return redirect(url_for('upload_file'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
