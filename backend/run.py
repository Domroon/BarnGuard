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

BASE_PATH = Path(os.getcwd()) 
TARGETS = {
    "video": BASE_PATH / "video-data" / "new",
    "thumbnail": BASE_PATH / "thumbnail_pics",
    "video-move": BASE_PATH / "video-data",
}

ALLOWED_EXTENSIONS = {'mp4'}

connex_app = config.connexion_app

connex_app.add_api("swagger.yml")


def generate_thumbnail(video_path, thumbnail_path):
    print(f'Get Thumbnail Picture from the Video: "{video_path}"')
    with VideoFileClip(str(video_path)) as video:
        frame = video.get_frame(0)
    thumbnail_jpg = Image.fromarray(frame)
    print(f'Save Thumbnail Picture at: "{thumbnail_path}"')
    thumbnail_jpg.save(thumbnail_path)


def manage_thumbnails():
    print(f'[START] [THUMBNAIL GENERATOR]')
     # videonames are a random hash number
    while True:
        dir_list = os.listdir(TARGETS["video"])
        if dir_list:
            video_path = TARGETS["video"] / dir_list[0]
            thumbnail_path = (TARGETS["thumbnail"] / video_path.name).with_suffix('.jpg')
            generate_thumbnail(video_path, thumbnail_path)

            # move the videofile out of new-Folder
            destination_folder = TARGETS["video-move"]
            print(f'Move Video to "{destination_folder}"')
            shutil.move(video_path, destination_folder)
        else:
            print(f'[WAIT] for new Upload')
            break


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


@connex_app.route('/videos/<path:filename>', methods=['GET', 'POST'])
def single_video(filename):
    videos = os.path.join(os.getcwd(), flask_app.config['VIDEO_FOLDER'])
    return send_from_directory(directory=videos, filename=filename)


@connex_app.route('/thumbnail/<path:filename>', methods=['GET', 'POST'])
def single_thumbnail(filename):
    thumbnails = os.path.join(os.getcwd(), flask_app.config['THUMBNAIL_FOLDER'])
    return send_from_directory(directory=thumbnails, filename=filename)


@connex_app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "400"
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(flask_app.config['VIDEO_FOLDER'], filename))
        manage_thumbnails()
        return "200"
    else:
        return "415"


def main():
    connex_app.run(host='0.0.0.0', port=5000, debug=True)
    

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    main()
