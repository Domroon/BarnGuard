from flask import send_from_directory
from flask import render_template, request
from config import flask_app
import os

import config

ALLOWED_EXTENSIONS = {'mp4'}

connex_app = config.connexion_app

connex_app.add_api("swagger.yml")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return flask_app.send_static_file('index.html')

@connex_app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def single_video(filename):
    uploads = os.path.join(os.getcwd(), flask_app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@connex_app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(flask_app.config['UPLOAD_FOLDER'], filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def main():
    connex_app.run(host='0.0.0.0', port=5000, debug=True)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()
