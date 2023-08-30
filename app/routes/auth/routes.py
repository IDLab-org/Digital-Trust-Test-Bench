from flask import current_app, render_template, url_for, redirect, session, flash
from app.routes.auth import bp
from app.routes.auth.forms import BasicLoginForm
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
    form = BasicLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
      
        # -- Calling the DTT service  API
        jsonparams = {"email": email, "password": password}

        response = DTT_service.request(method='post', route='/login', json_params=jsonparams, api_token='')
        
        # TBD: The DTT-Service login will eventually return a meaningful error code - currently, it only returns code 200
        # and true if login worked; false if not
        # anything else is interpreted as a failed connection
        if response.text == 'true': 
            session["online"] = True
            flash (f'You are logged in as {email}')
            return render_template("pages/index.jinja") 
        elif response.text == 'false': 
            flash ('Invalid credentials. Please try again')
            return redirect(url_for("auth.login"))
        else:
            flash ('DTT Service not available. Come back later')
            return redirect(url_for("auth.login"))


        return render_template("pages/index.jinja") 

    return render_template("pages/basic_login.jinja", form=form)


@bp.route("/logout", methods=["GET"])
def logout():
    session["online"] = False
    return redirect(url_for("auth.login"))
