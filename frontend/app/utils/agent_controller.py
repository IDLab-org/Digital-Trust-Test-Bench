from flask import current_app, render_template, session
from datetime import datetime
from app.utils import qr_codes
import json, requests


def credential_offer(email):
    dt = datetime.now()
    dt = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = current_app.config["ACCOUNT_CREDENTIAL_OFFER"]
    payload["credential"]["credentialSubject"] = {
        "email": email,
        "join_date": dt,
        "full_name": email.split("@")[0],
        "organization": email.split("@")[1],
    }
    # Create a credential offer exchange record
    r = requests.post(
        f"{current_app.config['VC_API_ENDPOINT']}/workflows/credential-offer?anoncreds=True",
        json=payload,
    )
    exchange_url = r.json()["exchange-url"]
    offer_qr_code = qr_codes.generate(exchange_url)
    return offer_qr_code


def proof_request(payload):
    r = requests.post(
        f"{current_app.config['VC_API_ENDPOINT']}/workflows/presentation-request?anoncreds=True",
        json=payload,
    )
    exchange_url = r.json()["exchange-url"]
    proof_qr_code = qr_codes.generate(exchange_url)
    return proof_qr_code


def create_verifiable_presentation():
    credential = render_template(
        "credentials/dttUser.jinja", email=email, issuance_date=dt
    )
    credential = json.loads(credential)
    payload = {"credential": credential, "options": {}}
    r = requests.post(
        f"{current_app.config['VC_API_ENDPOINT']}/credentials/issue", json=payload
    )
    verifiable_credential = r.json()["verifiableCredential"]
    verifiable_presentation = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1",
        ],
        "type": "VerifiablePresentation",
        "verifiableCredential": [verifiable_credential],
    }
    verifiable_presentation = json.dumps(verifiable_presentation)
    return verifiable_presentation

def verify_presentation():
    r = requests.get(
        f"{current_app.config['AGENT_ADMIN_ENDPOINT']}/present-proof-2.0/records/{session['presentation_exchange']}"
    )
    if r.json().get("verified") and r.json()["verified"]:
        return True
    return False