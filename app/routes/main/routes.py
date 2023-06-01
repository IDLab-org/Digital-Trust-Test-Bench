from flask import current_app, render_template, url_for, redirect, session, request, flash, send_file
from app.routes.main import bp
import json, requests, secrets, base64
from pprint import pprint

@bp.before_request
def before_request_callback():
    if "online" not in session or not session["online"]:
        session['invitation'] = "https://xyz"
        return redirect(url_for("auth.logout"))

@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "pages/auth.jinja", 
        title="Demo"
        )