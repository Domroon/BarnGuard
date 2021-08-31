from flask import render_template
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion

from flask_cors import CORS #ONLY for Development!!


# This creates the connexion application instance.
connexion_app = connexion.App(__name__)

# Read the swagger.yml file to configure the endpoints
#connexion_app.add_api('swagger.yml')

# This gets the underlying Flask app instance.
flask_app = connexion_app.app  # Flask(__name__)
flask_app.static_folder = '../build'
flask_app.static_url_path = '/'
CORS(flask_app) #ONLY for Development!!

flask_app.config['SECRET_KEY'] = 'ugasgfiiggfgiiasf657sff'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
flask_app.config['SQLALCHEMY_ECHO'] = True
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['VIDEO_FOLDER'] = 'video-data/new'
flask_app.config['VIDEO_FOLDER_PROCESSED'] = 'video-data'
flask_app.config['THUMBNAIL_FOLDER'] = 'thumbnail_pics'
db = SQLAlchemy(flask_app)

# Initialize Marshmallow
ma = Marshmallow(flask_app)
