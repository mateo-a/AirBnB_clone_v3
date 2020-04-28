#!/usr/bin/python3
""" API v1 """
from models import storage
from api.v1.views import app_views
from flask import Flask
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(close):
    """ Close the session """
    storage.close()

if __name__ == "__main__":
    h = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') else '0.0.0.0'
    p = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') else 5000
    app.run(host=h, port=p, threaded=True)
