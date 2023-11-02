from flask import current_app, render_template, url_for, redirect, session, request, flash, send_file
from app.routes.main import bp
from app.utils.session_check import Session_check

@bp.before_request
def before_request_callback():
  # if not Session_check.check_online(session):
  #       return redirect(url_for("auth.logout"))
  pass

@bp.route("/", methods=["GET"])
def index():
    if not Session_check.check_online(session):
          return redirect(url_for("auth.logout"))
    return render_template("pages/index.jinja", title="Dashboard | DTT")

@bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_file("static/favicon.png", mimetype='image/gif')
