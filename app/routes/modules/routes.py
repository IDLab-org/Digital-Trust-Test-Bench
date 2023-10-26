from flask import current_app, render_template, url_for, redirect, session, request, flash, send_file
from app.routes.modules import bp
import json, requests, secrets, base64
from pprint import pprint
from app.utils.session_check import Session_check
from app.routes.modules.forms import VCFormatValidatorV1, VCProfilerV1
from app.routes.modules import tests
from werkzeug.utils import secure_filename

@bp.before_request
def before_request_callback():
  pass
  # if not Session_check.check_online(session):
  #       return redirect(url_for("auth.logout"))

@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/modules/index.jinja", title="Modules | DTT")

@bp.route("/w3c", methods=["GET"])
def w3c():
    print("hello")
    form = VCFormatValidatorV1()
    form.features.choices = [
        ("schema", "Schema"),
        ("refresh", "Refresh"),
        ("evidence", "Evidence"),
        ("status", "Status"),
        ("tou", "Terms of Use")
    ]
    form.proof_type.choices = [("", "")]+[
        ("ldp", "Linked Data Proof"),
        ("jwt", "JSON Web Token"),
        ("zkp", "Zero Knowledge Proof")
    ]
    return render_template("pages/modules/w3c/index.jinja", form=form, title="W3C Module | DTT")

@bp.route("/w3c/vc-test-suite", methods=["GET", "POST"])
def vc_validator_v1():
    form = VCFormatValidatorV1()
    form.proof_type.choices = [("", "")]+[
        ("ldp", "Linked Data Proof"),
        # ("jwt", "JSON Web Token"),
        ("zkp", "Zero Knowledge Proof")
    ]
    # with open("app/static/data/vc/example.jsonld", "r") as f:
    #     form.vc_text.data = f.read()
    if request.method == "POST":
        vc_doc = json.loads(form.vc_text.data)
        features = ["schema", "refresh", "evidence", "status", "tou", "ldp", "jwt", "zkp"]
        if vc_doc.get("credentialStatus"):
            features.remove("status")
        if vc_doc.get("credentialSchema"):
            features.remove("schema")
        if vc_doc.get("refreshService"):
            features.remove("refresh")
        if vc_doc.get("termsOfUse"):
            features.remove("tou")
        if vc_doc.get("evidence"):
            features.remove("evidence")
        if form.proof_type.data:
            features.remove(form.proof_type.data)
        # print(request.files["file_vc"])
        # file_name = secure_filename()
        data = {
            "workspace_id": session['user_info']['workspace'],
            "verifiable_credential": vc_doc,
            "unsupported_features": features
        }
        # r = requests.post(f'{current_app.config["DTT_MODULES_URL"]}/test-suites/w3c/vc-test-suite', json=data)
        # return render_template("pages/modules/w3c/vc-test-suite-results.jinja", form=form, title="VC-Validator 1.1 | DTT")
    return render_template("pages/modules/w3c/vc-test-suite.jinja", form=form, title="VC-Validator 1.1 | DTT")

@bp.route("/w3c/vc-profiler/1.1", methods=["GET", "POST"])
def vc_profiler_v1():
    form = VCProfilerV1()
    with open('app/static/data/vc/example.jsonld', "r") as f:
        form.vc.data = f.read()
    vc_profile = {}
    if request.method == "POST":
        vc = form.vc.data
        vc = json.loads(vc)
        # vc_profile = tests.vc_profiler(vc)
        supported_features = {
            "basic": True,
            "schema": True if vc.get("credentialSchema") else False,
            "refresh": True if vc.get("refreshService") else False,
            "evidence": True if vc.get("evidence") else False,
            "status": True if vc.get("credentialStatus") else False,
            "tou": True if vc.get("termsOfUse") else False,
            "ldp": False,
            "jwt": False,
            "zkp": False,
        }
    return render_template("pages/modules/w3c/vc_profiler_v1.jinja", form=form, vc_profile=vc_profile, title="VC-Profiler | DTT")

@bp.route("/w3c/vc-api", methods=["GET", "POST"])
def vc_api():
    form = VCProfilerV1()
    with open('app/static/data/vc_exmple.jsonld', "r") as f:
        form.vc.data = f.read()
    if request.method == "POST":
        pass
    return render_template("pages/modules/w3c/vc_api.jinja", form=form, title="VC-API | DTT")