from datetime import datetime as DateTime
from datetime import timezone
from random import randint
from secrets import token_urlsafe


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


def gen_random_time():
    # date
    rand_day = str(randint(0,30))
    if len(rand_day) == 1:
        rand_day = f"0{rand_day}"
    rand_month = str(randint(1, 12))
    if len(rand_month) == 1:
        rand_month = f"0{rand_month}"
    rand_year = "2021"

    rand_date = f"{rand_day}.{rand_month}.{rand_year}"

    # time
    rand_hour = str(randint(0, 23))
    if len(rand_hour) == 1:
        rand_hour = f"0{rand_hour}"
    rand_minute = str(randint(0,59))
    if len(rand_minute) == 1:
        rand_minute = f"0{rand_minute}"

    rand_time = f"{rand_hour}:{rand_minute}"

    return rand_date , rand_time


# implement a function that generate a json-object for a post-request to the server (use requests)


def main():
    print("Date Time now")
    date, time = generate_formatted_timestamp()
    print(date)
    print(time)
    print()
    print("Random Date Time")
    rand_date, rand_time = gen_random_time()
    print(rand_date)
    print(rand_time)
    print()
    print("videoname")
    videoname = token_urlsafe(8)
    print(videoname + ".mp4")
    print()
    print("thumbnail_photo")
    thumbnail_photo = videoname + ".jpg"
    print(thumbnail_photo)
    

if __name__ == '__main__':
    main()
