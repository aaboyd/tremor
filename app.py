from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import db, Record
import os


app = Flask(__name__)

db_path = os.path.realpath( os.path.join(os.path.dirname(__file__), 'data.db') );

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path;

db.init_app(app)

@app.before_first_request
def build_db():
    db.create_all();

@app.route('/')
def hello():
    return "Hello, World!";