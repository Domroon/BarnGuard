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


# implement a function that generate a json-object for a post-request to the server (use requests)


def main():
    BASE_PATH = Path(getcwd())
    path = BASE_PATH /"videos"
    upload_ready = BASE_PATH / "upload_ready"

    while True:
        dir_list = listdir(path=path)
        if dir_list:
            print("Video found!")

            # generate random name
            raw_video_name = f'{token_urlsafe(8)}'
            videoname = f'{raw_video_name}.mp4'

            # rename first video
            video_path = path / dir_list[0]
            new_video_path = path / videoname
            try:
                os.rename(video_path, new_video_path)

                # move video
                shutil.move(new_video_path, upload_ready / videoname)

                # upload video
                url = "http://localhost:5000/upload"
                files = {'file' : open(str(upload_ready/videoname), 'rb')}
                r = requests.post(url, files=files)
                if r.status_code == 200:
                    print(f'{videoname} sucessfully uploaded')
                    print(f'status-code: {r.status_code}')
                    files.clear()
                    os.remove(upload_ready / videoname)
                else:
                    print(f'Can not upload {videoname}')
                    print(f'Response Code: {r.status_code}')
                    print(f'Response Body:')
                    print(r.text)
            except PermissionError:
                print("PermissionError")

            # delete video after upload
            # generate json-object and send with POST-request to server
            rand_date, rand_time = gen_random_datetime()

            url = "http://localhost:5000/api/videos"
            payload = json.dumps(generate_video_json(rand_date, rand_time, raw_video_name))
            r = requests.post(url, data=payload, headers={'Content-Type': 'application/json'})
            print(f'Post Json-Data for {videoname}')
            print(f'POST: {payload}')
            print(f'Response Code {r.status_code}')
            print(f'Response Body:')
            print(r.text)

        time.sleep(1)
            

    # print("Date Time now")
    # date, time = generate_formatted_timestamp()
    # print(date)
    # print(time)
    # print()
    # print("Random Date Time")
    # rand_date, rand_time = gen_random_datetime()
    # print(rand_date)
    # print(rand_time)
    # print()
    # print("videoname")
    # 
    # print(videoname + ".mp4")
    # print()
    # print("thumbnail_photo")
    # thumbnail_photo = videoname + ".jpg"
    # print(thumbnail_photo)
    

if __name__ == '__main__':
    main()
