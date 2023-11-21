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
from app.routes.test_suites import bp
from app.utils.session_check import Session_check
from app.routes.test_suites.forms import (
    DataModelFormV1,
    VcTestSuiteFormV1,
    VcPlaygroundTestSuiteForm,
)
from werkzeug.utils import secure_filename
import json, requests, textwrap
from time import sleep
from pprint import pprint


@bp.before_request
def before_request_callback():
    if not Session_check.check_online(session):
        return redirect(url_for("auth.logout"))


@bp.route("/", methods=["GET"])
def index():
    return render_template("pages/test_suites/index.jinja", title="test_suites | DTT")


@bp.route("/report", methods=["GET"])
def report():
    project_id = request.args.get("project_id")
    workspace_id = session["workspace_id"]
    r = requests.get(
        f'{current_app.config["DTT_SERVICE_URL"]}/reports/render?project_id={project_id}&workspace_id={workspace_id}'
    )
    r = r.text
    r = r.replace("\\", "")
    return r


@bp.route("/data-model", methods=["GET", "POST"])
def data_model():
    form = DataModelFormV1()
    report_url = url_for("test_suites.report", project_id="data-model")
    vc_profile = None
    with open("app/static/data/vc/example.jsonld", "r") as f:
        vc_example = f.read()
    vc_example = json.loads(vc_example)
    if request.method == "POST":
        vc = json.loads(form.vc_text.data)
        data = {"workspace_id": session["workspace_id"], "verifiable_credential": vc}
        r = requests.post(
            f'{current_app.config["DTT_SERVICE_URL"]}/test-suites/data-model', json=data
        )
        vc_profile = r.json()
        sleep(8)
    return render_template(
        "pages/test_suites/data_model.jinja",
        form=form,
        title="Data Model | DTT",
        data_to_copy=vc_example,
        report_url=report_url,
        vc_profile=vc_profile,
    )


@bp.route("/vc-test-suite", methods=["GET", "POST"])
def vc_test_suite():
    form = VcTestSuiteFormV1()
    report_url = url_for("test_suites.report", project_id="vc-test-suite")
    # form.implementation.choices = [("", "")] + [
    #     ("https://vc-api.dtt-cloud.idlab.app", "IDLab"),
    #     ("https://uniissuer.io/1.0/credentials", "Danube Tech"),
    #     ("https://interop.connect.trinsic.cloud/vc-api", "Trinsic"),
    #     ("https://issuer-vcs.sandbox.trustbloc.dev/vc-issuer-interop-key", "SecureKey")
    # ]
    form.features.choices = [
        ("schema", "Schema"),
        ("refresh", "Refresh Service"),
        ("evidence", "Evidence"),
        ("status", "Status"),
        ("tou", "Terms of Use"),
    ]
    form.proof_type.choices = [
        ("ldp", "Linked Data Proof"),
        ("jwt", "JSON Web Token"),
        ("zkp", "Zero Knowledge Proof"),
    ]
    if request.method == "POST":
        all_features = [
            "basic",
            "schema",
            "refresh",
            "evidence",
            "status",
            "tou",
            "ldp",
            "jwt",
            "zkp",
        ]
        supported_features = ["basic"] + form.features.data + [form.proof_type.data]
        unsupported_features = list(set(all_features) - set(supported_features))
        # if form.implementation.data:
        #     endpoint = form.implementation.data
        # else:
        endpoint = form.endpoint.data
        data = {
            "workspace_id": session["workspace_id"],
            "endpoint": endpoint,
            "token": form.token.data,
            "unsupported_features": unsupported_features,
        }
        requests.post(
            f'{current_app.config["DTT_SERVICE_URL"]}/test-suites/vc-test-suite',
            json=data,
        )
        sleep(8)
    return render_template(
        "pages/test_suites/vc_test_suite.jinja",
        form=form,
        title="VC Test Suite | DTT",
        report_url=report_url,
    )


@bp.route("/vc-playground-test-suite", methods=["GET", "POST"])
def vc_playground_test_suite():
    form = VcPlaygroundTestSuiteForm()
    report_url = url_for("test_suites.report", project_id="vc-playground-test-suite")
    # form.implementation.choices = [("", "")] + [
    #     ("https://vc-api.dtt-cloud.idlab.app", "IDLab"),
    #     ("https://interop.connect.trinsic.cloud/vc-api", "Trinsic"),
    #     ("https://issuer-vcs.sandbox.trustbloc.dev/vc-issuer-interop-key", "SecureKey"),
    #     ("https://uniissuer.io/1.0", "Danube Tech")
    # ]
    # form.verifier.choices = [("", "")] + [
    #     ("https://platform.interop.mattrlabs.io/vc-http-api/v1/credentials/verify", "Mattr")
    # ]
    if request.method == "POST":
        # if form.implementation.data:
        #     endpoint = form.implementation.data
        # else:
        endpoint = form.endpoint.data
        issuer = {
            "id": "Test",
            "label": "Test",
            "endpoint": endpoint + "/credentials/issue",
        }
        verifier = {
            "id": "Test",
            "label": "Test",
            "endpoint": endpoint + "/credentials/verify",
        }
        data = {
            "workspace_id": session["workspace_id"],
            "issuer": issuer,
            "verifier": verifier,
        }
        requests.post(
            f'{current_app.config["DTT_SERVICE_URL"]}/test-suites/vc-playground-test-suite',
            json=data,
        )
        sleep(8)
    return render_template(
        "pages/test_suites/vc_playground.jinja",
        form=form,
        title="Test Suites | DTT",
        report_url=report_url,
    )
