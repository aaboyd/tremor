# Tremor

*This is a code sample written by [Alex Boyd](http://alexboyd.me), any comments / questions / concerns are welcome, just drop in a github issue.  You can find my resume at [Alex Boyd's Resume](http://sdrv.ms/1b2GXeJ).*

[![Build Status](https://travis-ci.org/aaboyd/tremor.png?branch=master)](https://travis-ci.org/aaboyd/tremor)
[![Coverage Status](https://coveralls.io/repos/aaboyd/tremor/badge.png?branch=master)](https://coveralls.io/r/aaboyd/tremor?branch=master)

----

**Note : Written in Windows, sorry about any platform related issues**


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

## Date's are always UTC
In general python's default date implementation is not complete, to avoid having to code against the date changing, just assuming everything is UTC.

## Optimizations are not a priority at this point
In general nothing is optimized, there are probably faster and better ways to filter, sort, and execute different queries, but this implementation was quick to show some coding abilities.

# Work still to be done
There is not a lot of tests for mixing different parameters.  Logging has been stripped out and needs to be re-added with proper log statements not just ```print``` commands.  Probably a lot of other stuff that I am missing.


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

### Open up your browser
The project will read the environment variable PORT and use that, default is 5000.
Using the default, so http://localhost:5000/earthquakes.json should return data for all earthquakes.
