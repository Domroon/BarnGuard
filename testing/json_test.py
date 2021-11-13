from os import getcwd
from pathlib import Path
from datetime import datetime as DateTime
import json
from os import listdir

PATH = Path(getcwd())

def main():
    if 'test.json' not in listdir():
        with open('test.json', 'w+') as file:
            file.write(json.dumps([]))

    with open('test.json', 'r') as file:
        json_data = json.loads(file.read())

    if len(json_data) >= 1:
        # get the last object
        object_num = len(json_data) - 1
        print(json_data[object_num]['datetime'])
    else:
        print('File is empty')

    json_data.append({'datetime' : str(DateTime.now()), 'temperature' : 'Nothing'})

    with open('test.json', 'w') as file:
        file.write(json.dumps(json_data))
        
if __name__ == '__main__':
    main()