from moviepy.editor import VideoFileClip
from PIL import Image
import os
import shutil


BASE_PATH = os.getcwd() #+ '\\backend'


def generate_path(target):
    if target == "video":
        return BASE_PATH + '\\video-data\\new\\'
    elif target == "thumbnail":
        return BASE_PATH + '\\thumbnail_pics\\'
    elif target == "video-move":
        return BASE_PATH + '\\video-data\\'


def generate_thumbnail(video_path, thumbnail_path):
    video = VideoFileClip(video_path)
    frame = video.get_frame(0)
    thumbnail_jpg = Image.fromarray(frame)
    thumbnail_jpg.save(thumbnail_path)


def generate_thumbnail_name(videoname):
    split_video = videoname.split('.')
    return split_video[0] + '.jpg'

    
def main():
    # videonames are a random hash number
    videoname = "123.mp4" 
    # thumbnail names are the same name as the video (only data-format ending is another)
    thumbnail_name = generate_thumbnail_name(videoname) 

    video_path = f'{generate_path("video")}{videoname}'
    thumbnail_path = f'{generate_path("thumbnail")}{thumbnail_name}'
    print()
    print(f'Get Thumbnail Picture from: {video_path}')
    print()
    print(f'Save Thumbnail Picture at: {thumbnail_path}')
    print()

    generate_thumbnail(video_path, thumbnail_path)

    # move the videofile out of new-Folder
    destination_folder = generate_path("video-move")
    print(destination_folder)
    shutil.move(video_path, destination_folder)


if __name__ == '__main__':
    main()
