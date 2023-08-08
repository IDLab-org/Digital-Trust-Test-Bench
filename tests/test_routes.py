# tests/test_auth.py

from flask import current_app, render_template, url_for, redirect, session
from app.routes.auth import bp
import pytest
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

# Create a test Flask application
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    return app

# Test the 'index' route
def test_index_route(client):
    response = client.get(url_for('auth.index'))
    # Check if the response status code is 200 (success)
    assert response.status_code == 200
    # Check if the page contains the word "Login"
    assert b'Login' in response.data

# Test the 'login' route
def test_login_route(client):
    response = client.get(url_for('auth.login'))
    # Check if the response status code is 302 (redirect)
    assert response.status_code == 302
    # Check if the redirected URL is the 'index' route URL
    assert response.headers['Location'] == url_for('auth.index', _external=True)

# Test the 'logout' route
def test_logout_route(client):
    response = client.get(url_for('auth.logout'), follow_redirects=True)
    # Check if the response status code is 200 (success)
    assert response.status_code == 200
    # Check if the page contains the word "Login" after the logout
    assert b'Login' in response.data
