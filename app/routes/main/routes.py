from flask import current_app, render_template, url_for, redirect, session, request, flash, send_file
from app.routes.main import bp
import json, requests, secrets, base64
from pprint import pprint
from app.utils.session_check import Session_check

@bp.before_request
def before_request_callback():
  if not Session_check.check_online(session):
        return redirect(url_for("auth.logout"))

@bp.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("auth.login"))

@bp.route("/home", methods=["GET"])
def home():
    return render_template("pages/index.jinja")