from datetime import datetime as DateTime
from secrets import token_urlsafe
import os
from os import getcwd, listdir
from pathlib import Path
import time
import shutil
import requests
import json
import logging
import sys
import time
import subprocess
import threading
import traceback

from moviepy.editor import VideoFileClip
from PIL import Image
from python_tsl2591 import tsl2591
import smbus2
import bme280

try:
    import RPi.GPIO as GPIO
    import picamera
except ModuleNotFoundError as error:
    print(f'{error}\nPlease run the Program on a RaspberryPi')
    sys.exit()

from ina219 import INA219


NETWORK_ADDRESS="domroon.de" # development: localhost:5000
UPLOAD_URL = f'http://{NETWORK_ADDRESS}/upload'
JSON_URL = f'http://{NETWORK_ADDRESS}/api/videos'
BASE_PATH = Path(getcwd())
FILES_UPLOAD = BASE_PATH / "files_upload"
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
MIN_MOVEMENT = 3
MOVE_PERIOD = 10 # seconds


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
        self.logger.debug(f'CAPTURED video "{self.name}"')
        self._convert()
        self._generate_thumbnail()
        self._move_thumbnailfile()
        self._move_videofile()

    def _move_videofile(self):
        self.logger.debug(f'MOVE "{self.name}"\nfrom {BASE_PATH}\nto {FILES_UPLOAD}')
        shutil.move(str(BASE_PATH / f'{self.name}.mp4'), str(FILES_UPLOAD / f'{self.name}.mp4'))

    def _generate_thumbnail(self):
        self.logger.debug(f'CREATE thumbnail for video "{self.name}"')
        with VideoFileClip((str(BASE_PATH / f'{self.name}.mp4'))) as videofile:
            frame = videofile.get_frame(0)
        self.thumbnail = Image.fromarray(frame)

    def _move_thumbnailfile(self):
        self.thumbnail.save(str(FILES_UPLOAD / f'{self.name}.jpg'))
        self.logger.debug(f'SAVED Thumbnail {self.name}.jpg at: {FILES_UPLOAD}')

    def _convert(self):
        self.logger.debug(f'CONVERT "{self.name}" from "h264" to "mp4"')
        subprocess.run(["MP4Box", "-add", f'{self.name}.h264', f'{self.name}.mp4'])
        os.remove(str(BASE_PATH / f'{self.name}.h264'))


class MovementDetector:
    def __init__(self, logger):
        self.logger = logger
        self._movement = False
        self._active = False
        self._sensor_thread = None
        self._movement_thread = None
        self._movement_counter = 0
        self._min_movements = MIN_MOVEMENT
        self._move_period = MOVE_PERIOD
        self.detected = False

    def start(self):
        self._sensor_thread = threading.Thread(target=self._detect)
        self._sensor_thread.daemon=True
        self._movement_thread = threading.Thread(target=self._detect_move)
        self._movement_thread.daemon=True
        self.logger.info("START motion Thread")
        self._sensor_thread.start()
        self._movement_thread.start()
    
    def _detect_move(self):
        while True:
            try:
                start_time = round(time.perf_counter())
                self._movement_counter = 0
                while True:
                    end_time = round(time.perf_counter()) - start_time
                    if end_time >= self._move_period:
                        self.logger.debug('reached move_period time - reset mov_counter and time')
                        break
                    if self._active:
                        self._movement_counter = self._movement_counter + 1
                        self.logger.debug(f'Movement Counter: {self._movement_counter}')
                    if self._movement_counter >= self._min_movements:
                        self.logger.info('DETECT Movement')
                        self.detected = True
                        break
                    time.sleep(1)
                time.sleep(1)
            except:
                save_error(self.logger)

    def _detect(self):
        while True:
            try:
                self._movement = GPIO.input(24)
                if self._movement and self._active == False:
                    self._active = True
                    time.sleep(1.5)
                elif self._movement == False and self._active == True:
                    self._active = False
            except:
                save_error(self.logger)

            time.sleep(0.1)


class SensorData:
    def __init__(self, logger):
        self.logger = logger
        self.tslDevice = tsl2591()
        #self.dhtDevice = adafruit_dht.DHT22(board.D23, use_pulseio=False)
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
            try:
                with open('sensors_data.json', 'r') as file:
                    json_data = json.loads(file.read())
                    self.logger.debug('GET all sensor data')
                    data_dict = self.sensors.read_all()
                    json_data.append(data_dict)

                with open('sensors_data.json', 'w') as file:
                    file.write(json.dumps(json_data))

                time.sleep(10)
            except:
                save_error(self.logger)

    def read_last_data(self):
        with open('sensors_data.json', 'r') as file:
            json_data = json.loads(file.read())

            if len(json_data) >= 1:
                # get the last object
                object_num = len(json_data) - 1
                return json_data[object_num]
            else:
                self.logger.error('Can not read last data. File is empty.')

        
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
                self.logger.debug(f'FOUND Video "{filename}"')
                self.logger.debug('GENERATE json-object')
                self.json_data = self._generate_json(filename)
                time.sleep(2)
                try:
                    self.logger.debug(f'UPLOAD Thumbnail Picture "{filename}.jpg"')
                    picture_resp = self._upload_media(f'{filename}.jpg')
                    self.logger.debug(f'UPLOAD Video "{filename}.mp4"')
                    video_resp = self._upload_media(f'{filename}.mp4')
                except requests.exceptions.ConnectionError as error:
                    self.logger.error(f'{error}. Try again in 10s.')
                except:
                    save_error(self.logger)

                try:
                    if picture_resp.status_code == 200 and video_resp.status_code == 200:
                        self.logger.debug('DELETE uploaded media files')
                        os.remove(str(FILES_UPLOAD / f'{filename}.mp4'))
                        os.remove(str(FILES_UPLOAD / f'{filename}.jpg'))
                        self.logger.debug(f'UPLOAD JSON-File')
                        json_resp = self._upload_json(json.dumps(self.json_data))
                        if json_resp.status_code != 201:
                            json_resp_text = json.loads(json_resp.text)
                            self.logger.error(f'{json_resp.status_code} - {json_resp_text["title"]} - {json_resp_text["detail"]}')
                        else:
                            self.logger.info(f'UPLOAD for "{filename}" successfully')
                    else:
                        self.logger.error(f'Video Response: {video_resp}; Picture Response: {picture_resp}. JSON-Data will not uploaded.')
                except:
                    save_error(self.logger)
                
            time.sleep(10)

    def _search_video_filename(self):
        dirlist = listdir(str(FILES_UPLOAD))
        file_type = None
        i = 0
        while True:
            try:
                if len(dirlist) == i:
                    return None
                filename, file_type = dirlist[i].split('.')
                if file_type == 'mp4':
                    return filename
                i = i + 1
            except:
                save_error(self.logger)

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


def setup_GPIO(main_logger):
    try:
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
    except:
        save_error(main_logger)


def is_brightness_low(data, threshold):
    brightness = data.read_last_data()['brightness']

    if(brightness <= threshold):
        return True
    else:
        return False


def save_error(logger):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_string = '\n'
    for line in traceback_list:
        traceback_string += line
    logger.error(traceback_string) 
    raise


def main():
    # Configure Loggers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='wildcam.log', encoding='utf-8')
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    main_logger = logging.getLogger("Main")
    main_logger.setLevel(logging.INFO)
    main_logger.addHandler(console_handler)
    main_logger.addHandler(file_handler)

    video_logger = logging.getLogger("Video")
    video_logger.setLevel(logging.INFO)
    video_logger.addHandler(console_handler)
    video_logger.addHandler(file_handler)

    motion_logger = logging.getLogger("MovementDetector")
    motion_logger.setLevel(logging.INFO)
    motion_logger.addHandler(console_handler)
    motion_logger.addHandler(file_handler)

    sensors_logger = logging.getLogger("SensorData")
    sensors_logger.setLevel(logging.INFO)
    sensors_logger.addHandler(console_handler)
    sensors_logger.addHandler(file_handler)

    data_logger = logging.getLogger('Data')
    data_logger.setLevel(logging.INFO)
    data_logger.addHandler(console_handler)
    data_logger.addHandler(file_handler)

    transmit_logger = logging.getLogger('FileTransmitter')
    transmit_logger.setLevel(logging.INFO)
    transmit_logger.addHandler(console_handler)
    transmit_logger.addHandler(file_handler)

    main_logger.info("START wildcam software")

    if 'files_upload' not in listdir():
        os.mkdir(BASE_PATH / 'files_upload')
        main_logger.info('CREATED "files_upload" folder')
    else:
        main_logger.info('FOUND "files_upload" folder')

    setup_GPIO(main_logger)

    data = Data(data_logger, sensors_logger)
    data.start()
    motion_detector = MovementDetector(motion_logger)
    motion_detector.start()
    transmitter = FileTransmitter(transmit_logger)
    transmitter.start()

    recording = False
    while True:
        try:
            if motion_detector.detected and not recording:
                low_brightness = is_brightness_low(data, 5)
                main_logger.info(f'brightness: {low_brightness}')
                if low_brightness:
                    main_logger.info('ON LED Panel')
                    GPIO.output(25, True)
                    GPIO.output(12, True)
                video = Video(video_logger)
                video.record()
                del video
                recording = False
                if low_brightness:
                    main_logger.info('OFF LED Panel')
                    GPIO.output(25, False)
                    GPIO.output(12, False)
                motion_detector.detected = False
            time.sleep(0.5)
        except KeyboardInterrupt:
            raise
        except:
            save_error(main_logger)
        finally:
            GPIO.cleanup()
            main_logger.info("CLEAN all GPIO Pins")
            main_logger.info('TERMINATE "wildcam.py"')
            sys.exit()

    
if __name__ == '__main__':
    main()
