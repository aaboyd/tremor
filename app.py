from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import db, Record
import os


app = Flask(__name__)
app.config.from_object('settings.base');
app.config.from_envvar('FLASK_CONFIG');


db.init_app(app)

with app.app_context():
    db.create_all();

@app.route('/')
def hello():
    return "Hello, World!";