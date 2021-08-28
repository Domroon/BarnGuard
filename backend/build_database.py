import os
from config import db
from models import Video


# Delete database file if it exists currently
if os.path.exists('site.db'):
    os.remove('site.db')


# Create the database
db.create_all()


db.session.commit()