import os, json

from flask import Flask

from models import db

class InvalidArgumentError(Exception):
    pass;

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.base');

    if os.environ.get('FLASK_CONFIG') is not None:
        app.config.from_object(os.environ.get('FLASK_CONFIG'));

    db.init_app(app)

    with app.app_context():
        db.create_all();

    from routes.earthquakes import earthquakes
    app.register_blueprint(earthquakes)
    
    @app.errorhandler(InvalidArgumentError)
    def handle_sqlalchemy_assertion_error(err):
        return json.dumps( {'error':err.message} ), 400;

    return app;

app = create_app()