from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Settings

app.config.update({
    'SECRET_KEY': '123',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
})

db = SQLAlchemy(app)

from webapp.views import *
