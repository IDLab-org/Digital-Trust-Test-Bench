from flask import current_app, render_template, url_for, redirect, session, request, flash, send_file
from app.routes.test_suites import bp
from app.utils.session_check import Session_check
from app.routes.test_suites.forms import VCFormatValidatorV1, VCProfilerV1, VcTestSuiteFormV1
# from app.routes.test_suites import tests
from werkzeug.utils import secure_filename
import json, requests, textwrap
from time import sleep

@bp.before_request
def before_request_callback():
  if not Session_check.check_online(session):
        return redirect(url_for("auth.logout"))

@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/test_suites/index.jinja", title="test_suites | DTT")

@bp.route("/vc-test-suite", methods=["GET", "POST"])
def vc_test_suite():
    form = VcTestSuiteFormV1()
    report_url = url_for("test_suites.vc_test_suite_report")
    vc_profile = None
    with open("app/static/data/vc/example.jsonld", "r") as f:
        vc_example = f.read()
    vc_example = json.loads(vc_example)
    if request.method == "POST":
        vc = json.loads(form.vc_text.data)
        data = {
            "workspace_id": session['workspace_id'],
            "verifiable_credential": vc
        }
        r = requests.post(f'{current_app.config["DTT_SERVICE_URL"]}/test-suites/vc-test-suite', json=data)
        vc_profile = r.json()
        sleep(8)
        # count = 0
        # while count < 5:
        #     sleep(2)
        #     status = requests.get(f'{current_app.config["DTT_SERVICE_URL"]}/test-suites/vc-test-suite/status')
        #     if status != "completed":
        #         count =+ 1
        #         continue
        #     else:
        #         # report = 
        #         break
        # return render_template("pages/test_suites/w3c/vc-test-suite-results.jinja", form=form, title="VC-Validator 1.1 | DTT")
    return render_template("pages/test_suites/vc_test_suite.jinja", form=form, title="VC Test Suite | DTT", data_to_copy=vc_example, report_url=report_url, vc_profile=vc_profile)

@bp.route("/vc-test-suite/report", methods=["GET"])
def vc_test_suite_report():
    r = requests.get(f'{current_app.config["DTT_SERVICE_URL"]}/reports/render?project_id=vc-test-suite&workspace_id={session["workspace_id"]}')
    r = r.text
    r = r.replace("\\", "")
    return r