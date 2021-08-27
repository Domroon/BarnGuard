from datetime import datetime as DateTime
from datetime import timezone
from random import randint
import re
from secrets import token_urlsafe
import os
from os import getcwd, listdir
from pathlib import Path
import time
import shutil
import requests
import json

from requests.models import Response


BASE_PATH = Path(getcwd())
PATH = BASE_PATH / "videos"
UPLOAD_READY = BASE_PATH / "upload_ready"


def generate_formatted_timestamp():
    now = str(DateTime.now()).split(' ')

    # Date
    date_now = now[0]
    formatted_date = format_date(date_now)

    # Time
    time_now = now[1]    
    formatted_time = format_time(time_now)

    return formatted_date, formatted_time


def format_date(date_now):
    date_items = date_now.split('-')
    return f'{date_items[2]}.{date_items[1]}.{date_items[0]}'


def format_time(time_now):
    time_items = time_now.split(':')
    return f"{time_items[0]}:{time_items[1]}"


def gen_random_datetime():
    # date
    rand_day = str(randint(0,30))
    if len(rand_day) == 1:
        rand_day = f"0{rand_day}"
    rand_month = str(randint(1, 12))
    if len(rand_month) == 1:
        rand_month = f"0{rand_month}"
    rand_year = "2021"

    rand_date = f"{rand_day}.{rand_month}.{rand_year}"

    # time
    rand_hour = str(randint(0, 23))
    if len(rand_hour) == 1:
        rand_hour = f"0{rand_hour}"
    rand_minute = str(randint(0,59))
    if len(rand_minute) == 1:
        rand_minute = f"0{rand_minute}"

    rand_time = f"{rand_hour}:{rand_minute}"

    return rand_date , rand_time


def generate_video_json(date, time, raw_video_name):
    json_data = {
        "date": date,
        "thumbnail_photo" : f'{raw_video_name}.jpg',
        "time" : time,
        "videoname" : f'{raw_video_name}.mp4',
    }
    return json_data


def rename_and_move_video(dir_list, videoname):
    # rename first video
    video_path = PATH / dir_list[0]
    new_video_path = PATH / videoname
    os.rename(video_path, new_video_path)

    # move video
    shutil.move(new_video_path, UPLOAD_READY / videoname)


def upload_video(videoname):
    url = "http://localhost:5000/upload"
    files = {'file' : open(str(UPLOAD_READY/videoname), 'rb')}
    return requests.post(url, files=files)

    # if r.status_code == 200:
    #     print(f'{videoname} sucessfully uploaded')
    #     print(f'Response Code: {r.status_code}')
    #     files.clear()
    #     os.remove(UPLOAD_READY / videoname)
    # else:
    #     print(f'Can not upload {videoname}')
    #     print(f'Response Code: {r.status_code}')
    #     print(f'Response Body:')
    #     print(f'{r.text}')


def upload_video_json(date, time, raw_video_name):
    url = "http://localhost:5000/api/videos"
    payload = json.dumps(generate_video_json(date, time, raw_video_name))
    return requests.post(url, data=payload, headers={'Content-Type': 'application/json'})

    # print(f'Post Json-Data for {raw_video_name}.mp4')
    # print(f'POST: {payload}')
    # print(f'Response Code {r.status_code}')
    # print(f'Response Body:')
    # print(r.text)


def show_response(resp : Response):
    print(f'[RESPONSE CODE] {resp.status_code}')
    print(f'[RESPONSE BODY] {resp.text}')


# correct the if-query and delete the video at sucessfully upload
def upload(videoname, raw_video_name):
    video_response = upload_video(videoname)
    print("[VIDEO RESPONSE]")
    show_response(video_response)

    # in production datetime.now() !!!
    rand_date, rand_time = gen_random_datetime()
    json_video_response = upload_video_json(rand_date, rand_time, raw_video_name)
    print("[VIDEO_JSON RESPONSE]")
    show_response(json_video_response)

    if video_response.status_code != 200 and json_video_response.status_code != 201:
        return True
    else:
        return False


def main():
    while True:
        dir_list = listdir(path=PATH)

        if dir_list:
            first_videoname = dir_list[0]
            print(f"[FOUND VIDEO] {first_videoname}")

            # generate random name
            raw_video_name = f'{token_urlsafe(8)}'
            videoname = f'{raw_video_name}.mp4'

            rename_and_move_video(dir_list, videoname)
            print(f'[RENAME] "{first_videoname}" to "{videoname}"')

            # try to upload until the internet connection is back
            while True:
                success = upload(videoname, raw_video_name)
                if success:
                    break
            print("Exit the Upload Loop")

        time.sleep(1)
            

if __name__ == '__main__':
    main()
