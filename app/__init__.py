from flask import Flask
app = Flask(__name__)
from app import views
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config.from_pyfile(os.path.join(parent_dir, 'config.py'))
