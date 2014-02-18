# Tremor
[![Build Status](https://travis-ci.org/aaboyd/tremor.png?branch=master)](https://travis-ci.org/aaboyd/tremor)
A simple application and solution to [a coding challenge](https://gist.github.com/bmarini/23c235aef10714d22a54).

Implementation is written in python with the help of :

-	[Flask](http://flask.pocoo.org/)
-	[Twisted](https://twistedmatrix.com/trac/)
-	[Requests](http://docs.python-requests.org/en/latest/index.html)
-	[Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
-	[SQLAlchemy](http://www.sqlalchemy.org/)

# Assumptions

## Data from the usgs source will always be in reverse chronological order
The importer uses the data to determine if a result is new or has already been imported

## Eqid is a unique value
It is used as the PrimaryKey for each record

## Date's will never be in a different format than UTC
In general python's default date implementation is not complete, to avoid having to code against the date changing, just assuming everything is UTC.

## Optimizations are not necessary right now
In general nothing is optimized, there are probably faster and better ways to filter, sort, and execute different queries, but this implementation was quick to show some coding abilities.

# Running and Testing
## Install Requirements
```
pip install -r requirements.txt
```

## Run Tests
```
coverage run -include=./**/* test.py --verbose
```

## View Coverage Results
```
coverage report -m
```

## Run project
```
python run.py
```