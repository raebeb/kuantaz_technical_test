from flask import Flask
from flask_json import FlaskJSON
from .config import *

app = Flask(__name__)
FlaskJSON(app)

# Routes go here
