import os
from config import db
from models import Video

# Data to initialize database with
VIDEO_DATA = [
    {
      "date": "42.08.2021",
      "time": "14:29",
      "thumbnail_photo": "martin_square.jpg",
      "videoname": "video_1"
    },
    {
      "date": "15.08.2021",
      "time": "12:41",
      "thumbnail_photo": "alles-theurer-logo.png",
      "videoname": "video_2"
    },
    {
      "date": "12.08.2021",
      "time": "12:15",
      "thumbnail_photo": "yt.jpg",
      "videoname": "video_3"
    },
    {
      "date": "16.08.2021",
      "time": "20:02",
      "thumbnail_photo": "martin.jpg",
      "videoname": "video_4"
    },
  ]

# Delete database file if it exists currently
if os.path.exists('site.db'):
    os.remove('site.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for video in VIDEO_DATA:
    p = Video(date=video['date'], time=video['time'], thumbnail_photo=video['thumbnail_photo'], videoname=video['videoname'])
    db.session.add(p)

db.session.commit()