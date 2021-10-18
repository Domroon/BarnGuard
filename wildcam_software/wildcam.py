from datetime import datetime as DateTime
import datetime
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
import logging

from requests.models import Response


BASE_PATH = Path(getcwd())
PATH = BASE_PATH / "videos"
UPLOAD_READY = BASE_PATH / "upload_ready"

# development "localhost:5000"
# deploy "domroon.de"
NETWORK_ADDRESS="domroon.de"


# create logger
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler ans set level to debug
fh = logging.FileHandler(filename='wildcam.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)


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
    rand_day = randint(1,29)
    rand_month = randint(1, 12)
    rand_year = 2021

    rand_date = str(datetime.date(rand_year, rand_month, rand_day))

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
    try:
        url = f'http://{NETWORK_ADDRESS}/upload'
        video_file = open(str(UPLOAD_READY/videoname), 'rb')
        files = {'file' : video_file}

        r = requests.post(url, files=files, headers={'Authorization' : 'gAAAAABhMhDkkS0ZWFKyrhFBnDxJp5r_cjV-ZXFYh4adcoCMRSwo_qcnfsqadt4nwD3XXBlYXNHNBJWyEB7FeH6qR_FVnxFa-NGLI2HPGBYCnY2avAdd5UJ1fBOR5YoVVR5O7iXE9rpnZKRWdkUAsyQ5zuQA_XquSukJvwziExE6a5TW4NTw3xQ='})

        video_file.close()

        if r.status_code == 200:
            os.remove(UPLOAD_READY / videoname)
    except Exception as error:
        logger.error(f'Upload Video Error: \n{error}')
        raise error

    return r

    
def upload_video_json(date, time, raw_video_name):
    try:
        url = f'http://{NETWORK_ADDRESS}/api/videos'
        payload = json.dumps(generate_video_json(date, time, raw_video_name))
        return requests.post(url, data=payload, headers={'Content-Type': 'application/json', 'Authorization' : 'gAAAAABhMhDkkS0ZWFKyrhFBnDxJp5r_cjV-ZXFYh4adcoCMRSwo_qcnfsqadt4nwD3XXBlYXNHNBJWyEB7FeH6qR_FVnxFa-NGLI2HPGBYCnY2avAdd5UJ1fBOR5YoVVR5O7iXE9rpnZKRWdkUAsyQ5zuQA_XquSukJvwziExE6a5TW4NTw3xQ='})
    except Exception as error:
        logger.error(f'Upload Video Json Error: \n{error}')
        raise error

    # print(f'Post Json-Data for {raw_video_name}.mp4')
    # print(f'POST: {payload}')
    # print(f'Response Code {r.status_code}')
    # print(f'Response Body:')
    # print(r.text)


# correct the if-query and delete the video at sucessfully upload
def upload(videoname, raw_video_name):
    video_response = upload_video(videoname)
    logger.info(f'VIDEO RESPONSE: \nRESPONSE CODE: {video_response.status_code}\nRESPONSE BODY: "{video_response.text}"')
    
    # in production datetime.now() !!!
    #rand_date, rand_time = gen_random_datetime()
    date = str(DateTime.now()).split()[0]
    long_time = str(DateTime.now()).split()[1]
    time=long_time.split('.')[0]
    json_video_response = upload_video_json(date, time, raw_video_name)
    logger.info(f'VIDEO_JSON RESPONSE: \nRESPONSE CODE: {json_video_response.status_code}\nRESPONSE BODY: "{json_video_response.text}"')

    if video_response.status_code != 200 and json_video_response.status_code != 201:
        return True
    else:
        return False


def main():
    while True:
        dir_list = listdir(path=PATH)

        if dir_list:
            first_videoname = dir_list[0]
            logger.info(f'FOUND VIDEO "{first_videoname}"')

            # generate random name
            raw_video_name = f'{token_urlsafe(8)}'
            videoname = f'{raw_video_name}.mp4'

            # try to rename until the authorization is there
            while True:
                try:
                    rename_and_move_video(dir_list, videoname)
                    logger.info(f'RENAME "{first_videoname}" to "{videoname}"')
                    break
                except PermissionError:
                    logger.error(f'PERMISSION ERROR "Try again in 1s"')
                    time.sleep(1)

            # try to upload until the internet connection is back
            while True:
                try:
                    print()
                    logger.info(f'UPLOAD START "{videoname}"')
                    upload(videoname, raw_video_name)
                    logger.info(f'UPLOAD END "{videoname}"')
                    break
                except requests.exceptions.ConnectionError as error:
                    logger.error(f'CONNECTION ERROR Try again in 5s: \n {error}')
                    time.sleep(5)
                except FileNotFoundError:
                    logger.error(f'FileNotFoundError "The file has already been uploaded"')
                    break
                except PermissionError:
                    logger.error(f'PERMISSION ERROR "Try again in 0.5s"')
                    time.sleep(0.5)
                except Exception as error:
                    logger.error(error)
                    raise error

        time.sleep(1)
            

if __name__ == '__main__':
    main()
