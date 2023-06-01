from flask import current_app, render_template, url_for, redirect, session
from app.routes.auth import bp
import json, requests, secrets
from pprint import pprint

@bp.before_request
def before_request_callback():
    pass

@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/auth.jinja", title="Login")

@bp.route("/login", methods=["GET"])
def login():
    return redirect(url_for("auth.index"))

@bp.route("/logout", methods=["GET"])
def logout():
    session["online"] = False
    return redirect(url_for("auth.index"))