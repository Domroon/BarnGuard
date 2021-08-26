import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image
import os

BASE_PATH = Path(os.getcwd()) 
TARGETS = {
    "video": BASE_PATH / "video-data" / "new",
    "thumbnail": BASE_PATH / "thumbnail_pics",
    "video-move": BASE_PATH / "video-data",
}

def generate_thumbnail(video_path, thumbnail_path):
    with VideoFileClip(str(video_path)) as video:
        frame = video.get_frame(0)
    thumbnail_jpg = Image.fromarray(frame)
    thumbnail_jpg.save(thumbnail_path)

def main():
    # videonames are a random hash number
    video_path = TARGETS["video"] / "reit.mp4" 
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
