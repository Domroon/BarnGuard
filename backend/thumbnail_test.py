import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image
<<<<<<< HEAD

BASE_PATH = Path('.') #+ '\\backend'
=======
import os

BASE_PATH = Path(os.getcwd()) 
>>>>>>> 2fd3fbe31c28dc20a413086cc28d75b30a03b03a
TARGETS = {
    "video": BASE_PATH / "video-data" / "new",
    "thumbnail": BASE_PATH / "thumbnail_pics",
    "video-move": BASE_PATH / "video-data",
}

def generate_thumbnail(video_path, thumbnail_path):
<<<<<<< HEAD
    with VideoFileClip(video_path) as video:
=======
    with VideoFileClip(str(video_path)) as video:
>>>>>>> 2fd3fbe31c28dc20a413086cc28d75b30a03b03a
        frame = video.get_frame(0)
    thumbnail_jpg = Image.fromarray(frame)
    thumbnail_jpg.save(thumbnail_path)

def main():
    # videonames are a random hash number
<<<<<<< HEAD
    video_path = TARGETS["video"] / "123.mp4" 
=======
    video_path = TARGETS["video"] / "reit.mp4" 
>>>>>>> 2fd3fbe31c28dc20a413086cc28d75b30a03b03a
    thumbnail_path = (TARGETS["thumbnail"] / video_path.name).with_suffix('.jpg')
    print()
    print(f'Get Thumbnail Picture from: {video_path}')
    print()
    print(f'Save Thumbnail Picture at: {thumbnail_path}')
    print()

    generate_thumbnail(video_path, thumbnail_path)
    # move the videofile out of new-Folder
    destination_folder = TARGETS["video-move"]
    print(destination_folder)
    shutil.move(video_path, destination_folder)

if __name__ == '__main__':
    main()