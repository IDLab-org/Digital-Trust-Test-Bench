from flask import (
    current_app,
    render_template,
    url_for,
    redirect,
    session,
    request,
    flash,
    send_file,
)
from app.routes.main import bp
from app.utils.session_check import Session_check
import requests


@bp.before_request
def before_request_callback():
    if not Session_check.check_online(session):
        return redirect(url_for("auth.logout"))


@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/index.jinja", title="Dashboard | DTT")


@bp.route("/reports", methods=["GET"])
def reports():
    # r = requests.get(f"http://allure.{session['workspace_id']}:5050")
    r = requests.get(f"http://localhost:5050/projects")
    projects = [project for project in r.json()["data"]["projects"]]
    return render_template(
        "pages/reports.jinja", title="Dashboard | DTT", projects=projects
    )


@bp.route("/reports/{project_id}", methods=["GET"])
def project_report(project_id: str):
    if not Session_check.check_online(session):
        return redirect(url_for("auth.logout"))
    # r = requests.get(f"http://allure.{session['workspace_id']}:5050")
    r = requests.get(f"http://localhost:5050/latest-report?project_id={project_id}")
    r = requests.get(f"http://localhost:5050/generate-report?project_id={project_id}")
    r = requests.get(
        f"http://localhost:5050/emailable-report/render?project_id={project_id}"
    )
    r = requests.get(f"http://localhost:5050/projects/{project_id}")
    r = requests.get(f"http://localhost:5050/projects/{project_id}/path")
    return render_template("pages/reports.jinja", title="Dashboard | DTT")
