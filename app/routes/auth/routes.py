from flask import current_app, render_template, url_for, redirect, session, flash, request
from app.routes.auth import bp
from app.routes.auth.forms import BasicLoginForm, GithubLoginForm
import json, requests, secrets
from pprint import pprint
from config import Config
from app.utils.session_check import Session_check
from app.utils.DTT_service import DTT_service

@bp.before_request
def before_request_callback():
    pass
    ### Do not call the Session_check here because of infinite recursion
    

@bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = GithubLoginForm()
 
    return render_template("pages/login.jinja", form=form)

@bp.route("/logout", methods=["GET"])
def logout():
    session["online"] = False
    if "authorization_header" in session:  # This is the Authorization token provided by DTT-Service upon login
        session.pop("authorization_header")
    if "DTT_user_info" in session:  # This is the Authorization token provided by DTT-Service upon login
        session.pop("DTT_user_info")
    return redirect(url_for("auth.login"))



#--  Following 2 routes are for github login

# '/github_login' - Starts the login process
# calls DTT Service's /auth/github/authorize (no parameters)
# That API will return a redirect URL with some parameters  - That URL goes to github's authorization API 
# which in turn will also reditect users to the 2nd route below: /github-callback
@bp.route('/github_login', methods=['GET'])
def github_login():
   # Call DTT Service's Authorize API
   # TBD: Create URI with config parameters - Create new function in utils/DTT_service to form the URL
    response = DTT_service.request(method='get', route='/auth/github/authorize')
    if response.status_code != 200:
        flash({
            "title": "Service Unavailiable",
            "error": response.status_code,
            "message": "DTT service is currently unavailiable"
        })    
        return redirect(url_for("auth.login"))  # TBD - Redirect to a better error page
    
    elif 'authorization_url' not in response.json():
        flash({
            "title": "Service Unavailiable",
            "error": response.status_code,
            "message": "No authorization URL returned"
        })    

    authorize_url=response.json()['authorization_url']

    return redirect(authorize_url)

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
@bp.route('/github-callback', methods=['GET'])
def github_callback():
    code = request.args.get('code', default = 0, type = str)
    state = request.args.get('state', default = 'NoState', type = str)

    # Now call the DTT service's callback function from here
    response = DTT_service.request(method='get', route=f'/auth/github/callback?code={code}&state={state}')

    if response.status_code != 200:
        flash({
            "title": "Service Unavailiable",
            "error": response.status_code,
            "message": "GitHub callback error"
        })
        return redirect(url_for("auth.login"))

    # extract the token
    elif 'access_token' not in response.json():
        flash({
            "title": "Service Unavailiable",
            "error": response.status_code,
            "message": "No token returned"
        })
        return redirect(url_for("auth.login"))

    token= response.json()['access_token']
    # Create the Authorization header and store it into this user's session
    # Subsequent cals to DTT Service shall use this header
    authorization_header = {"Authorization": f"Bearer {token}"}
    session["authorization_header"] = authorization_header
    session["online"] = True

    # Now call the service to get the current user's basic info from FastAPI_Users
    # This returns the content of the user's record in DTT-Service's "User" table 
    # TBD:  in DTT-Service, most useful user properties should be added into the User table. 
    #       This would prevent us from having to perform other calls (specifically /users/github-user)
    #       So this /users/me call should return all necessary user data
    response = DTT_service.request(method='get', route=f'/users/me', api_token=session["authorization_header"])  
    DTT_user_info = response.json()
    
    if 'id' not in DTT_user_info:
        flash({
            "title": "Service Unavailiable",
            "error": response.status_code,
            "message": "No user id returned from /users/me"
        })
        return redirect(url_for("auth.login"))

    info_userID = DTT_user_info['id']

    # call the service to get my info from github
    # Data returned includes several user properties as described in 
    # https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user 
    # https://docs.github.com/en/rest/users/emails?apiVersion=2022-11-28#list-email-addresses-for-the-authenticated-user
    # For more details: See https://idlab-org.atlassian.net/wiki/spaces/DTT/pages/1309900880/Login+with+github+-+Implementation+Notes
    response = DTT_service.request(method='get', route=f'/users/github-user', api_token=session["authorization_header"])  
    github_profile=response.json()
    DTT_user_info['github_profile'] = github_profile
    # all user info gets stored into the session object
    session['DTT_user_info'] = DTT_user_info
    session['current_user'] = DTT_user_info

    return redirect(url_for("main.home"))

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
