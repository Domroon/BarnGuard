import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import time

BASE_PATH = Path(os.getcwd()) 
TARGETS = {
    "video": BASE_PATH / "video-data" / "new",
    "thumbnail": BASE_PATH / "thumbnail_pics",
    "video-move": BASE_PATH / "video-data",
}

def generate_thumbnail(video_path, thumbnail_path):
    print(f'Get Thumbnail Picture from the Video: "{video_path}"')
    with VideoFileClip(str(video_path)) as video:
        frame = video.get_frame(0)
    thumbnail_jpg = Image.fromarray(frame)
    print(f'Save Thumbnail Picture at: "{thumbnail_path}"')
    thumbnail_jpg.save(thumbnail_path)

def main():
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
            print(f'[WAIT] 5s')
            time.sleep(5)
            print(f'[CHECK FOR NEW VIDEOS]')


if __name__ == '__main__':
    main()