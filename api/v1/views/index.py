#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""

from models import storage
from flask import Flask
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})
