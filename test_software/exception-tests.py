import time
import sys
import traceback

while True:
    try:
        print("here")
        time.sleep(2)
        raise TypeError
    except KeyboardInterrupt:
        raise
    except:
        tb = sys.exc_info()[2]
        error = traceback.extract_tb(tb)
        print(str(error.format()))