from flask import send_from_directory
from flask import render_template, request
from config import flask_app
import os
import config
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image
import time
import shutil

import connexion
import six
from werkzeug.exceptions import Unauthorized
from jose import JWTError, jwt
import logging


BASE_PATH = Path(os.getcwd())
TARGETS = {
    "video": BASE_PATH / "video-data" / "new",
    "thumbnail": BASE_PATH / "thumbnail_pics",
    "video-move": BASE_PATH / "video-data",
}

ALLOWED_EXTENSIONS = {'mp4', 'jpg'}

JWT_ISSUER = 'com.zalando.connexion'
JWT_SECRET = 'change_this'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

# LOGGER
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename='flask_server.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

connex_app = config.connexion_app

connex_app.add_api("swagger.yml")

logger.info("START")

def generate_thumbnail(video_path, thumbnail_path):
    print(f'Get Thumbnail Picture from the Video: "{video_path}"')
    try:
        with VideoFileClip(str(video_path)) as video:
            frame = video.get_frame(0)
        thumbnail_jpg = Image.fromarray(frame)
        logger.debug(f'Save Thumbnail Picture at: "{thumbnail_path}"')
        thumbnail_jpg.save(thumbnail_path)
    except Exception as error:
        logger.error(error)
        raise error


def manage_thumbnails():
    logger.info('generate thumbnail')
     # videonames are a random hash number
    try:
        while True:
            dir_list = os.listdir(TARGETS["video"])
            if dir_list:
                video_path = TARGETS["video"] / dir_list[0]
                thumbnail_path = (TARGETS["thumbnail"] / video_path.name).with_suffix('.jpg')
                # wait until the video is fully downloaded!
                # logger.warning('Wait 10s to be sure the Video is fully downloaded')
                time.sleep(10)
                generate_thumbnail(video_path, thumbnail_path)

                # move the videofile out of new-Folder
                destination_folder = TARGETS["video-move"]
                logger.debug(f'Move Video to "{destination_folder}"')
                shutil.move(str(video_path), str(destination_folder))
            else:
                logger.info('wait for new upload')
                break
    except Exception as error:
        logger.error(error)
        raise error


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    logger.debug('send index.html')
    return flask_app.send_static_file('index.html')


@connex_app.route('/videos/<path:filename>', methods=['GET', 'POST'])
def single_video(filename):
    videos = os.path.join(os.getcwd(), flask_app.config['MEDIA_FOLDER'])
    logger.debug("get single video")
    return send_from_directory(directory=videos, filename=filename)


@connex_app.route('/thumbnail/<path:filename>', methods=['GET', 'POST'])
def single_thumbnail(filename):
    logger.debug('get thumbnail')
    thumbnails = os.path.join(os.getcwd(), flask_app.config['MEDIA_FOLDER'])
    return send_from_directory(directory=thumbnails, filename=filename)


@connex_app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logger.warning('no video-file or jpeg-file in post-request "/upload"')
            return "400"
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(flask_app.config['MEDIA_FOLDER'], filename))
        # manage_thumbnails()
        return "200"
    else:
        logger.warning('videotype or picturetype in post-request "/upload" is not correct')
        return "415"


def generate_token(user_id):
    logger.debug("generate token")
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _current_timestamp() -> int:
    return int(time.time())


def main():
    # host='0.0.0.0', port="5000", debug=True for test purposes
    # host='domroon.de', port=80, debug=False in Deploy Mode
    try: 
        connex_app.run(host='0.0.0.0', port="5000", debug=True)
    except Exception as error:
        logger.error(error)
        raise error 


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()
