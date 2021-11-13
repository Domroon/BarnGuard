import requests
import os
from pathlib import Path
from os import getcwd, listdir
from datetime import datetime as DateTime
import json
import time
import logging
import threading


NETWORK_ADDRESS="domroon.de"
UPLOAD_URL = f'http://{NETWORK_ADDRESS}/upload'
JSON_URL = f'http://{NETWORK_ADDRESS}/api/videos'
BASE_PATH = Path(getcwd())
FILES_UPLOAD = BASE_PATH / "files_upload"


class FileTransmitter:
    def __init__(self, logger):
        self.logger = logger
        self.json_data = None

    def start(self):
        thread = threading.Thread(target=self._transmit)
        thread.daemon = True
        self.logger.info('START FileTransmitter Thread')
        thread.start()

    def _transmit(self):
        while True:
            picture_resp = None
            video_resp = None
            filename = self._search_video_filename()
            if filename:
                self.logger.info(f'FOUND Video "{filename}"')
                self.logger.info('GENERATE json-object')
                self.json_data = self._generate_json(filename)
                time.sleep(2)
                try:
                    self.logger.info(f'UPLOAD Thumbnail Picture "{filename}.jpg"')
                    picture_resp = self._upload_media(f'{filename}.jpg')
                    self.logger.info(f'UPLOAD Video "{filename}.mp4"')
                    video_resp = self._upload_media(f'{filename}.mp4')
                except requests.exceptions.ConnectionError as error:
                    self.logger.error(f'{error}. Try again in 10s.')
                if picture_resp.status_code == 200 and video_resp.status_code == 200:
                    self.logger.info('DELETE uploaded media files')
                    os.remove(str(FILES_UPLOAD / f'{filename}.mp4'))
                    os.remove(str(FILES_UPLOAD / f'{filename}.jpg'))
                    self.logger.info(f'UPLOAD JSON-File')
                    json_resp = self._upload_json(json.dumps(self.json_data))
                    if json_resp.status_code != 201:
                        json_resp_text = json.loads(json_resp.text)
                        self.logger.error(f'{json_resp.status_code} - {json_resp_text["title"]} - {json_resp_text["detail"]}')
                else:
                    self.logger.error(f'Video Response: {video_resp}; Picture Response: {picture_resp}. JSON-Data will not uploaded.')
            time.sleep(10)

    def _search_video_filename(self):
        dirlist = listdir(str(FILES_UPLOAD))
        file_type = None
        i = 0
        while True:
            if len(dirlist) == i:
                return None
            filename, file_type = dirlist[i].split('.')
            if file_type == 'mp4':
                return filename
            i = i + 1

    def _generate_json(self, filename):
        now = str(DateTime.now()).split(' ')

        date_now = now[0]
        date = self._format_date(date_now)

        time_now = now[1]    
        time = self._format_time(time_now)

        json_data = {
            "date": date,
            "thumbnail_photo" : f'{filename}.jpg',
            "time" : time,
            "videoname" : f'{filename}.mp4',
        }
        return json_data

    def _format_date(self, date_now):
        date_items = date_now.split('-')
        return f'{date_items[0]}-{date_items[1]}-{date_items[2]}'

    def _format_time(self, time_now):
        time_items = time_now.split(':')
        return f"{time_items[0]}:{time_items[1]}"

    def _upload_media(self, filename):
        with open(str(FILES_UPLOAD / filename ), 'rb') as file:
            files = {'file' : file}
            r = requests.post(UPLOAD_URL, files=files, headers={'Authorization' : 'gAAAAABhMhDkkS0ZWFKyrhFBnDxJp5r_cjV-ZXFYh4adcoCMRSwo_qcnfsqadt4nwD3XXBlYXNHNBJWyEB7FeH6qR_FVnxFa-NGLI2HPGBYCnY2avAdd5UJ1fBOR5YoVVR5O7iXE9rpnZKRWdkUAsyQ5zuQA_XquSukJvwziExE6a5TW4NTw3xQ='})   
        return r

    def _upload_json(self, json_data):
        r = requests.post(JSON_URL, data=json_data, headers={'Content-Type': 'application/json', 'Authorization' : 'gAAAAABhMhDkkS0ZWFKyrhFBnDxJp5r_cjV-ZXFYh4adcoCMRSwo_qcnfsqadt4nwD3XXBlYXNHNBJWyEB7FeH6qR_FVnxFa-NGLI2HPGBYCnY2avAdd5UJ1fBOR5YoVVR5O7iXE9rpnZKRWdkUAsyQ5zuQA_XquSukJvwziExE6a5TW4NTw3xQ='})
        return r


def main():
    # Configure Loggers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='upload_test.log', encoding='utf-8')
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    transmit_logger = logging.getLogger('FileTransmitter')
    transmit_logger.setLevel(logging.DEBUG)
    transmit_logger.addHandler(console_handler)
    transmit_logger.addHandler(file_handler)

    transmitter = FileTransmitter(transmit_logger)
    transmitter.start()

    while True: 
        time.sleep(5)


if __name__ == '__main__':
    main()