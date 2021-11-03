import requests
import os
from pathlib import Path
from os import getcwd, listdir
from datetime import datetime as DateTime
import json
import time

NETWORK_ADDRESS="domroon.de"
BASE_PATH = Path(getcwd())
FILES_UPLOAD = BASE_PATH / "files_upload"

def upload_video(filename):
    try:
        url = f'http://{NETWORK_ADDRESS}/upload'
        video_file = open(str(FILES_UPLOAD/filename), 'rb')
        files = {'file' : video_file}

        r = requests.post(url, files=files, headers={'Authorization' : 'gAAAAABhMhDkkS0ZWFKyrhFBnDxJp5r_cjV-ZXFYh4adcoCMRSwo_qcnfsqadt4nwD3XXBlYXNHNBJWyEB7FeH6qR_FVnxFa-NGLI2HPGBYCnY2avAdd5UJ1fBOR5YoVVR5O7iXE9rpnZKRWdkUAsyQ5zuQA_XquSukJvwziExE6a5TW4NTw3xQ='})

        video_file.close()

        if r.status_code == 200:
            os.remove(str(FILES_UPLOAD/filename))
    except Exception as error:
        print(f'Upload Video Error: \n{error}')
        raise error

    return r


def upload(videoname, raw_video_name):
    video_response = upload_video(videoname)
    print(f'VIDEO RESPONSE: \nRESPONSE CODE: {video_response.status_code}\nRESPONSE BODY: "{video_response.text}"')
    
    # in production datetime.now() !!!
    #rand_date, rand_time = gen_random_datetime()
    date = str(DateTime.now()).split()[0]
    long_time = str(DateTime.now()).split()[1]
    time=long_time.split('.')[0]
    json_video_response = upload_video_json(date, time, raw_video_name)
    print(f'VIDEO_JSON RESPONSE: \nRESPONSE CODE: {json_video_response.status_code}\nRESPONSE BODY: "{json_video_response.text}"')

    if video_response.status_code != 200 and json_video_response.status_code != 201:
        return True
    else:
        return False


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


def generate_json_file(date, time, filename):
    filename, file_type = filename.split('.')
    if file_type == 'mp4':
        json_data = {
            "date": date,
            "thumbnail_photo" : f'{filename}.jpg',
            "time" : time,
            "videoname" : f'{filename}.mp4',
        }
        return json_data
    else:
        return 'wrong file type'


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
    return f'{date_items[0]}-{date_items[1]}-{date_items[2]}'


def format_time(time_now):
    time_items = time_now.split(':')
    return f"{time_items[0]}:{time_items[1]}"


def main():
    #upload_video('ruehrwerk.jpg')
    # print(listdir('files_upload'))
    while True: 
        datetime = generate_formatted_timestamp()
        print(generate_json_file(datetime[0], datetime[1], 'test.jpeg'))
        time.sleep(1)

# baue hier direkt FileTransmitter, welcher seine operationen in einem eigenen Thread ausführt! Falls eine Exception kommt, diese loggen und in 5s nochmal versuchen
# (Denn es kann ja sein, dass ein video noch nicht zuende kopiert ist)

# generiere json datei wenn der file-type mp4 ist (wenn nicht, dann erhöhe den zähler der gespeicherten liste von listdir() solange bis das listenende erreicht ist)
# lade das entsprechende video und entsprechende bildatei hoch
# wenn die antwort '200' ist, dann lade diese json-datei hoch, falls nicht -> beginne von vorne (listdir()- Abfrage)

if __name__ == '__main__':
    main()