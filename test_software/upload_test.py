import requests
import os
from pathlib import Path
from os import getcwd

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


def generate_video_json(date, time, filename):
    json_data = {
        "date": date,
        "thumbnail_photo" : f'{filename}.jpg',
        "time" : time,
        "videoname" : f'{filename}.mp4',
    }
    return json_data


def main():
    upload_video('ruehrwerk.jpg')


if __name__ == '__main__':
    main()