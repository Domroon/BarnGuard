from flask import send_from_directory
from flask import render_template
from config import flask_app
import os

import config

connex_app = config.connexion_app

connex_app.add_api("swagger.yml")

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

def main():
    connex_app.run(host='0.0.0.0', port=5000, debug=True)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()
