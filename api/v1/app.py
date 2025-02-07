#!/usr/bin/python3
"""API file to define the blueprint for endpoints """
from flask import Flask, jsonify, abort, make_response, Blueprint
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """handles teardown appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
