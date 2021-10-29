from datetime import datetime as DateTime
import datetime
from random import randint
from secrets import token_urlsafe
import os
from os import getcwd, listdir
from pathlib import Path
import time
import shutil
import requests
import json
import logging
import asyncio
import sys
import time
import subprocess
import threading

from moviepy.editor import VideoFileClip
from PIL import Image
from python_tsl2591 import tsl2591
import board
import adafruit_dht
import smbus2
import bme280
from ina219 import INA219
from ina219 import DeviceRangeError

try:
    import RPi.GPIO as GPIO
    import picamera
except ModuleNotFoundError as error:
    print(f'{error}\nPlease run the Program on a RaspberryPi')
    sys.exit()


BASE_PATH = Path(getcwd())
FILES_UPLOAD = BASE_PATH / "files_upload"

# development "localhost:5000"
# deploy "domroon.de"
NETWORK_ADDRESS="domroon.de"
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2


class Video:
    def __init__(self, logger, name=None, duration=10):
        self.name = name
        self.thumbnail = None
        self.record_datetime = None
        self.logger = logger
        self.duration = duration

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name == None:
            self._name = f'{token_urlsafe(8)}'
        else:
            self._name = name

    def record(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            # camera need time to start
            time.sleep(1)
            self.record_datetime = DateTime.now()
            camera.start_recording(f'{self.name}.h264')
            self.logger.info(f'CAPTURING video "{self.name}"')
            camera.wait_recording(self.duration)
            camera.stop_recording()
        self.logger.info(f'CAPTURED video "{self.name}"')
        self._convert()
        self._generate_thumbnail()
        self._move_thumbnailfile()
        self._move_videofile()

    def _move_videofile(self):
        self.logger.info(f'MOVE "{self.name}"\nfrom {BASE_PATH}\nto {FILES_UPLOAD}')
        shutil.move(str(BASE_PATH / f'{self.name}.mp4'), str(FILES_UPLOAD / f'{self.name}.mp4'))

    def _generate_thumbnail(self):
        self.logger.info(f'CREATE thumbnail for video "{self.name}"')
        with VideoFileClip((str(BASE_PATH / f'{self.name}.mp4'))) as videofile:
            frame = videofile.get_frame(0)
        self.thumbnail = Image.fromarray(frame)

    def _move_thumbnailfile(self):
        self.thumbnail.save(str(FILES_UPLOAD / f'{self.name}.jpg'))
        self.logger.info(f'SAVED Thumbnail {self.name}.jpg at: {FILES_UPLOAD}')

    def _convert(self):
        self.logger.info(f'CONVERT "{self.name}" from "h264" to "mp4"')
        subprocess.run(["MP4Box", "-add", f'{self.name}.h264', f'{self.name}.mp4'])
        os.remove(str(BASE_PATH / f'{self.name}.h264'))


class MovementDetector:
    def __init__(self, logger):
        self.logger = logger
        self.movement = False
        self.active = False
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self._detect)
        self.thread.daemon=True
        self.logger.info("START motion Thread")
        self.thread.start()

    def _detect(self):
        while True:
            self.logger.debug('movement detection is running')
            self.movement = GPIO.input(24)
            if self.movement and self.active == False:
                self.active = True
                self.logger.info("DETECTED motion")
            elif self.movement == False and self.active == True:
                self.active = False

            time.sleep(0.1)


class SensorData:
    def __init__(self, logger):
        self.logger = logger
        self.tslDevice = tsl2591()
        self.dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
        self.bme280Device = bme280.load_calibration_params(smbus2.SMBus(1), 0x76)
        self.solarDevice = INA219(SHUNT_OHMS, address=0x40)
        self.solarDevice.configure()
        self.powerbankDevice = INA219(SHUNT_OHMS, address=0x41)
        self.powerbankDevice.configure()
        self.extBatDevice = INA219(SHUNT_OHMS, address=0x44)
        self.extBatDevice.configure()

    def read_brightness(self):
        # unit: lux
        brightness = self.tslDevice.get_current()
        return round(brightness["lux"], 3) # integer?

    def read_dht(self):
        # unit: °C
        while True:
            try:
                temperature_c = self.dhtDevice.temperature
                humidity = self.dhtDevice.humidity
                return {'temperature:' : temperature_c, 'humidity' : humidity}
            except RuntimeError as error:
                self.logger.error(f'{error.args[0]}')
                time.sleep(2)
                continue
            except Exception as error:
                self.dhtDevice.exit()
                raise error

    def read_temperature(self):
        # unit: °C
        bme280_data = bme280.sample(smbus2.SMBus(1), 0x76, self.bme280Device)
        return bme280_data.temperature

    def read_pressure(self):
        # unit: hPa
        bme280_data = bme280.sample(smbus2.SMBus(1), 0x76, self.bme280Device)
        return bme280_data.pressure

    def read_solar_voltage(self):
        # unit: V
        return self.solarDevice.supply_voltage()

    def read_solar_current(self):
        # unit: mA
        return self.solarDevice.current()

    def read_powerbank_voltage(self):
        return self.powerbankDevice.supply_voltage()

    def read_powerbank_current(self):
        return self.powerbankDevice.current()

    def read_ext_bat_voltage(self):
        return self.extBatDevice.supply_voltage()

    def read_ext_bat_current(self):
        return self.extBatDevice.current()

    def read_all(self):
        self.logger.debug('READ all sensors')
        return {
            'datetime' : str(DateTime.now()),
            '950nm_led' : GPIO.input(25),
            '850nm_led' : GPIO.input(12),
            'brightness' : self.read_brightness(),
            'solar_panel' : GPIO.input(16),
            'solar_current' : round(self.read_solar_current()),
            'solar_voltage' : round(self.read_solar_voltage(), 3),
            'powerbank_current' : round(self.read_powerbank_current()),
            'powerbank_voltage' : round(self.read_powerbank_voltage(), 3),
            'ext_bat_current' : round(self.read_ext_bat_current()),
            'ext_bat_voltage' : round(self.read_ext_bat_voltage(), 3),
            'temperature' : round(self.read_temperature(), 1),
            'air_pressure' : round(self.read_pressure())
        }


class Data:
    def __init__(self, logger, sensors_logger):
        self.logger = logger
        self.sensors = SensorData(sensors_logger)

    def start(self):
        self._generate_json_file()
        thread = threading.Thread(target=self._save_sensor_data)
        thread.daemon = True
        self.logger.info("START sensor data Thread")
        thread.start()

    def _generate_json_file(self):
        if 'sensors_data.json' not in listdir():
            self.logger.info('GENERATE json-file "sensor_data.json"')
            with open('sensors_data.json', 'w+') as file:
                file.write(json.dumps([]))
        else:
            self.logger.info('FOUND json-file "sensor_data.json"')

    def _save_sensor_data(self):
        while True:
            with open('sensors_data.json', 'r') as file:
                json_data = json.loads(file.read())

            self.logger.debug('GET all sensor data')
            data_dict = self.sensors.read_all()
            json_data.append(data_dict)

            with open('sensors_data.json', 'w') as file:
                file.write(json.dumps(json_data))

            time.sleep(10)

    def read_last_data(self):
        with open('sensors_data.json', 'r') as file:
            json_data = json.loads(file.read())

        if len(json_data) >= 1:
            # get the last object
            object_num = len(json_data) - 1
            return json_data[object_num]
        else:
            self.logger.error('Can not read last data. File is empty.')

        
class TransmitFile:
    def __init__(self):
        pass


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


async def transmit_video_file():
    logger.info(f'WAITING for Videofile at "{PATH}"')
    while True:
        logger.debug('"transmit video" running')
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

        await asyncio.sleep(1)


def detect_movement():
    # logger.info("WAITING for movement")
    # GPIO.setmode(GPIO.BCM)
    # pin=24
    # GPIO.setup(pin, GPIO.IN)

    movement= 0
    active = 0

    try:
        while True:
            logger.debug('movement" running')
            movement = GPIO.input(24)

            if movement == 1 and active == 0:
                logger.info("movement detected")
                capture_video(VIDEO_DURATION)
                active = 1
            elif movement == 0 and active == 1:
                active = 0
        
            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()


def capture_video(duration):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        time.sleep(1)
        raw_video_name = f'{token_urlsafe(8)}'
        filename = f'{raw_video_name}.h264'
        end_filename = f'{raw_video_name}.mp4'
        camera.start_recording(filename)
        logger.info(f'START capturing video "{filename}"')
        camera.wait_recording(duration)
        camera.stop_recording()
        logger.info(f'END capturing video "{filename}"')

    subprocess.run(["MP4Box", "-add", f'{filename}', f'{end_filename}'])
    logger.info(f'CONVERTED "{raw_video_name}" from h264 to mp4 dataformat')
    
    shutil.move(str(BASE_PATH / end_filename), str(PATH))
    logger.info(f'MOVE "{end_filename}" to ./video')
    

def setup_GPIO(main_logger):

    GPIO.setmode(GPIO.BCM)

    # infrared motion detector
    GPIO.setup(24, GPIO.IN)

    # Relais for 950nm LEDs
    GPIO.setup(25, GPIO.OUT)

    # Relais for 850nm LEDs
    GPIO.setup(12, GPIO.OUT)

    # Relais for Solar Panel
    GPIO.setup(16, GPIO.OUT)
        
    main_logger.info("CONFIGURE all GPIO IN and OUTs sucessfully")


def is_brightness_low(data, threshold):
    brightness = data.read_last_data()['brightness']

    if(brightness <= threshold):
        return True
    else:
        return False


def main():
    # Configure Loggers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='wildcam.log', encoding='utf-8')
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    main_logger = logging.getLogger("main")
    main_logger.setLevel(logging.DEBUG)
    main_logger.addHandler(console_handler)
    main_logger.addHandler(file_handler)

    video_logger = logging.getLogger("video")
    video_logger.setLevel(logging.DEBUG)
    video_logger.addHandler(console_handler)
    video_logger.addHandler(file_handler)

    motion_logger = logging.getLogger("motion_detector")
    motion_logger.setLevel(logging.INFO)
    motion_logger.addHandler(console_handler)
    motion_logger.addHandler(file_handler)

    sensors_logger = logging.getLogger("sensors")
    sensors_logger.setLevel(logging.INFO)
    sensors_logger.addHandler(console_handler)
    sensors_logger.addHandler(file_handler)

    data_logger = logging.getLogger('data_saver')
    data_logger.setLevel(logging.INFO)
    data_logger.addHandler(console_handler)
    data_logger.addHandler(file_handler)

    main_logger.info("START wildcam software")

    if 'files_upload' not in listdir():
        os.mkdir(BASE_PATH / 'files_upload')
        main_logger.info('CREATED "files_upload" folder')
    else:
        main_logger.info('FOUND "files_upload" folder')

    setup_GPIO(main_logger)

    try:
        data = Data(data_logger, sensors_logger)
        data.start()
        motion_detector = MovementDetector(motion_logger)
        motion_detector.start()

        recording = False
        while True:
            if motion_detector.active and not recording:
                low_brightness = is_brightness_low(data, 5)
                main_logger.debug(f'brightness is low: {low_brightness}')
                if low_brightness:
                    main_logger.debug('put the lights on')
                    GPIO.output(25, True)
                    GPIO.output(12, True)
                recording = True
                video = Video(video_logger)
                video.record()
                del video
                recording = False
                time.sleep(1)
                if low_brightness:
                    main_logger.debug('put the lights off')
                    GPIO.output(25, False)
                    GPIO.output(12, False)
            time.sleep(1)
    finally:
        GPIO.cleanup()
        main_logger.info("CLEAN all GPIO Pins")

    # then implement solar loading

if __name__ == '__main__':
    main()
