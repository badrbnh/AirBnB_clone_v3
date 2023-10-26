#!/usr/bin/python3
"""Flask app"""
from flask import *
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
@app.teardown_appcontext
def close_storage(exception):
    """Close the storage session."""
    storage.close()

if __name__ == "__main__":
    host = '0.0.0.0' if not os.getenv('HBNB_API_HOST') else os.getenv('HBNB_API_HOST')
    port = 5000 if not os.getenv('HBNB_API_PORT') else int(os.getenv('HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)