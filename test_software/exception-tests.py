import time
import sys
import traceback
import logging


def save_error(logger):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_string = '\n'
    for line in traceback_list:
        traceback_string += line
    logger.error(traceback_string) 
    raise


def main():
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='test_logger.log', encoding='utf-8')
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    data_logger = logging.getLogger('Data')
    data_logger.setLevel(logging.INFO)
    data_logger.addHandler(console_handler)
    data_logger.addHandler(file_handler)

    while True:
        try:
            print("here")
            with open("file.txt", "r") as file:
                file.read()
        except KeyboardInterrupt:
            raise
        except:
            save_error(data_logger)
        time.sleep(2)


if __name__ == '__main__':
    main()