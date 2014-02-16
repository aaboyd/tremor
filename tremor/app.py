from flask import Flask, request
from sqlalchemy.ext.declarative import DeclarativeMeta
import os, json

from datetime import datetime
from dateutil.tz import tzutc

from models import db, Record



