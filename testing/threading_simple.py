import threading
from datetime import datetime as DateTime
import time

def main():
    
    name_1 = "thread 1"
    name_2 = "thread 2"
    try:
        thread_1 = threading.Thread(target=func_1, args=(name_1,))
        thread_2 = threading.Thread(target=func_1, args=(name_2,))
    
        thread_1.daemon=True
        thread_1.start()
        thread_2.daemon=True
        thread_2.start()
        #while True: time.sleep(100)
        while thread_1.is_alive(): 
            thread_1.join(1)  
    except (KeyboardInterrupt, SystemExit):
        print('\n! Received keyboard interrupt, quitting threads.\n')

    
def func_1(name):
    while True:
        print(f'{name}: {DateTime.now()}')
        time.sleep(1)


if __name__ == '__main__':
    main()