from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
import sys
from flask_cors import CORS #ONLY for Development!!


# This creates the connexion application instance.
connexion_app = connexion.App(__name__)

# Read the swagger.yml file to configure the endpoints
#connexion_app.add_api('swagger.yml')

# This gets the underlying Flask app instance.
flask_app = connexion_app.app  # Flask(__name__)
CORS(flask_app) #ONLY for Development!!

flask_app.config['SECRET_KEY'] = 'ugasgfiiggfgiiasf657sff'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
flask_app.config['SQLALCHEMY_ECHO'] = True
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)

# Initialize Marshmallow
ma = Marshmallow(flask_app)
