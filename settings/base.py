'''
    Python magic to get reference to file at ../data.db'
'''
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.realpath( os.path.join(os.path.dirname(__file__), '..', 'data.db') );