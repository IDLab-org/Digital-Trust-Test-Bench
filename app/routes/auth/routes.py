from flask import (
    current_app,
    render_template,
    url_for,
    redirect,
    session,
    flash,
    request,
)
from app.routes.auth import bp
import requests
from app import utilities
from app.utils.DTT_service import DTT_service
from app.utils.agent_controller import (
    credential_offer,
    proof_request
)


@bp.before_request
def before_request_callback():
    pass


@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():

    # Generate an example VC with a demo user
    offer_qr_code = credential_offer("demo.user@idlab.org")
    proof_qr_code = proof_request(current_app.config["LOGIN_PRESENTATION_REQUEST"])

    return render_template(
        "pages/login.jinja",
        title="Login | DTT",
        qr_presentation=proof_qr_code,
        qr_credential=offer_qr_code
    )


@bp.route("/vc_login", methods=["GET", "POST"])
def vc_login():
    r = requests.get(
        f"{current_app.config['AGENT_ADMIN_ENDPOINT']}/present-proof-2.0/records/{session['presentation_exchange']}"
    )
    # Check if the proof is verified
    if r.json().get("verified") and r.json()["verified"]:
        # Delete the presentation exchange record
        requests.delete(
            f"{current_app.config['AGENT_ADMIN_ENDPOINT']}/present-proof-2.0/records/{session['presentation_exchange']}"
        )
        # Grab the revealed email
        revealed_attributes = r.json()["by_format"]["pres"]["indy"]["requested_proof"][
            "revealed_attr_groups"
        ]["attrib_0"]["values"]
        session["user_info"] = {"email": revealed_attributes["email"]["raw"]}
        # Make sure the user workspace exist and provision it if it doesn't.
        # TODO change workspace label/id for a user_id
        data = {
            "workspace_type": "private",
            "workspace_label": session["user_info"]["email"],
        }
        r = requests.post(
            f"{current_app.config['DTT_SERVICE_URL']}/workspaces", json=data
        )
        session["workspace_id"] = r.json()["workspace_id"]
        session["online"] = True
        return redirect(url_for("main.index"))
    else:
        flash(
            {
                "title": "Verification failed",
                "error": None,
                "message": "Couldn't verify proof",
            }
        )
        return redirect(url_for("auth.login"))


# '/github_login' - Starts the login process
# calls DTT Service's /auth/github/authorize (no parameters)
# That API will return a redirect URL with some parameters  - That URL goes to github's authorization API
# which in turn will also reditect users to the 2nd route below: /github-callback
@bp.route("/github_login", methods=["GET"])
def github_login():
    # Call DTT Service's Authorize API
    # TBD: Create URI with config parameters - Create new function in utils/DTT_service to form the URL
    # response = DTT_service.request(method='get', route='/auth/github/authorize')
    r = DTT_service.request(method='get', route='/auth/github/authorize')
    if r.status_code != 200:
        flash(
            {
                "title": "Service Unavailiable",
                "error": r.status_code,
                "message": "DTT service is currently unavailiable",
            }
        )
        return redirect(url_for("auth.logout"))

    elif "authorization_url" not in r.json():
        flash(
            {
                "title": "Service Unavailiable",
                "error": r.status_code,
                "message": "No authorization URL returned",
            }
        )
        return redirect(url_for("auth.logout"))

    return redirect(r.json()["authorization_url"])


@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# --  Following 2 routes are for github login


# '/github-callback' is called after github's authorization page was displayed to the user and they accepted.
# This route is invoked as a redirect page by github's authorization function
# It needs to be registered in a github oauth app under: github > settings > Developer Settings > Oauth Apps
# 2 parameters:
#       code = Authorization code sent by github (a string)
#       state = State code created by DTT-Service's FastAPI User's code. Allows to link the callback with the proper original request
# This function here performs a lot:
#   - Calls the DTT-Service's /auth/github/callback API - which will call some github APIs to get minimal info about the current user and will also return an access token.
#       This access token is the auth token to be used in all subsequent calls to DTT-Service in the form of an Authorization token
#   - Creates a typical Authorization header and stores it in the session for subsequent calls
#   - Calls DTT-Service (/users/me) to get basic info about the current user . But this info is very minimal but it includes the current user ID in our database
#   - Calls DTT-service again (/users/github-user) to get more complete user info from github
#   - From all this info, the function creates a 'DTT_user_info' subdictionary in the session object, which also includes the user's
#       github profile ['github_profile'] which contains several user properties including their emails
@bp.route("/github-callback", methods=["GET"])
def github_callback():
    code = request.args.get("code", default=0, type=str)
    state = request.args.get("state", default="NoState", type=str)

    # Now call the DTT service's callback function from here
    response = DTT_service.request(
        method="get", route=f"/auth/github/callback?code={code}&state={state}"
    )

    if response.status_code != 200:
        flash(
            {
                "title": "Service Unavailiable",
                "error": response.status_code,
                "message": "GitHub callback error",
            }
        )
        return redirect(url_for("auth.logout"))

    # extract the token
    elif "access_token" not in response.json():
        flash(
            {
                "title": "Service Unavailiable",
                "error": response.status_code,
                "message": "No token returned",
            }
        )
        return redirect(url_for("auth.logout"))

    token = response.json()["access_token"]
    # Create the Authorization header and store it into this user's session
    # Subsequent cals to DTT Service shall use this header
    session["authorization_header"] = {"Authorization": f"Bearer {token}"}

    # Now call the service to get the current user's basic info from FastAPI_Users
    # This returns the content of the user's record in DTT-Service's "User" table
    # TBD:  in DTT-Service, most useful user properties should be added into the User table.
    #       This would prevent us from having to perform other calls (specifically /users/github-user)
    #       So this /users/me call should return all necessary user data
    response = DTT_service.request(
        method="get", route=f"/users/me", api_token=session["authorization_header"]
    )
    user_info = response.json()
    if "id" not in user_info:
        flash(
            {
                "title": "Service Unavailiable",
                "error": response.status_code,
                "message": "No user id returned from /users/me",
            }
        )
        return redirect(url_for("auth.login"))

    # call the service to get my info from github
    # Data returned includes several user properties as described in
    # https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user
    # https://docs.github.com/en/rest/users/emails?apiVersion=2022-11-28#list-email-addresses-for-the-authenticated-user
    # For more details: See https://idlab-org.atlassian.net/wiki/spaces/DTT/pages/1309900880/Login+with+github+-+Implementation+Notes
    response = DTT_service.request(
        method="get",
        route=f"/users/github-user",
        api_token=session["authorization_header"],
    )
    github_profile = response.json()
    email = utilities.get_primary_email(github_profile)

    # Store user information in the session
    session["user_info"] = {
        "email": email,
        "username": github_profile["login"],
        "organization": github_profile["company"],
    }

    # Make sure the user workspace exist and provision it if it doesn't
    data = {
        "workspace_type": "private",
        "workspace_label": session["user_info"]["email"],
    }
    r = requests.post(f"{current_app.config['DTT_SERVICE_URL']}/workspaces", json=data)
    session["workspace_id"] = r.json()["workspace_id"]
    session["online"] = True
    # Make sure the organization workspace exist and provision it if it doesn't
    # if session['user_info']['organization']:
    #     body = {
    #         "name": session['user_info']['organization'],
    #         "scope": "organization"
    #     }
    #     response = DTT_service.request(method='post', route=f'/workspaces', json_params=body, api_token=session["authorization_header"])

    # Create a credential offer for the user
    credential_offer = {
        "credentialSubject": session["user_info"],
        "credentialSchema": {
            "id": "RzWHypcqRZSB1prwXnApsS:2:DTTProfile:0.1",
            "definition": "RzWHypcqRZSB1prwXnApsS:3:CL:97127:IDLab DTT Profile",
        },
    }
    # r = requests.post('https://vc-api.dtt.idlab.app/workflows/credential-offer?anoncreds=True', json={"credential":credential_offer})
    # session["credential_offer"] = r.json()["exchange-url"]
    return redirect(url_for("main.index"))


# TEST function - auth/profile
#      left commented out since it provides examples on how to access user info
"""
@bp.route('/profile', methods=['GET'])
def user_profile():

    if "online" not in session:
        flash("User not logged in")
        return redirect(url_for("main.home"))
    
    if not session["online"]:
        flash("User not logged in. online=False")
        return redirect(url_for("main.home"))
   
    if "DTT_user_info" not in session:
        flash("github profile not found")
        return redirect(url_for("main.home"))
   
    DTT_user_info = session["DTT_user_info"]

    info_primary_email=DTT_user_info['email']
    for email in DTT_user_info['github_profile']['emails']:
        if email['primary']==True:
            info_primary_email=email['email']
   
    info_userID=DTT_user_info['id']
    if "login" not in DTT_user_info['github_profile']:
        info_login= 'unknown'
    else:
        info_login= DTT_user_info['github_profile']['login']

    if "name" not in DTT_user_info['github_profile']:
        info_name= 'unknown'
    else:
        info_name= DTT_user_info['github_profile']['name']

    if "company" not in DTT_user_info['github_profile']:
        info_company= 'unknown'
    else:
        info_company= DTT_user_info['github_profile']['company']

    flash(f"Profile: UserID={info_userID}")
    flash(f"githubLogin={info_login}")
    flash(f"name={info_name}")
    flash(f"primary_email={info_primary_email}") 
    flash(f"company={info_company} ")
    return redirect(url_for("main.home"))
"""
