import flask
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    verify_jwt_in_request, get_jwt_identity

from app import oauth
from app.user.repository import Repository
from app.user.service import Service

def login():
    if request.method == 'GET':
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id is None:
            return render_template('page/login.html')
        return redirect(url_for('home.public.index'))

    username = request.form.get('username')
    password = request.form.get('password')

    if not(username or password):
        flash('Missing username or password','error')
        return redirect(url_for('user.login'))

    try:
        result = Service.authenticate(username, password)
    except Exception as e:
        print('failed')
        flash(str(e),'error')
        return redirect(url_for('user.login'))

    resp = make_response(redirect(url_for('home.public.index')))
    set_access_cookies(resp, result['access_token'])
    set_refresh_cookies(resp, result['refresh_token'])
    return resp

def login_google():
    redirect_uri = url_for('user.google_auth',_external=True)
    return oauth.google.authorize_redirect(redirect_uri)

def google_auth():
    try:
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token, nonce=None)

        if user_info is None:
            flash('Could not get user info','error')
            return redirect(url_for('user.login'))

        result = Service.login_with_google(user_info)
        resp = make_response(redirect(url_for('home.public.index')))
        set_access_cookies(resp, result['access_token'])
        set_refresh_cookies(resp, result['refresh_token'])
        return resp
    except Exception as e:
        flash(str(e),'error')
        return redirect(url_for('user.login'))

def logout():
    session.clear()
    response = make_response(redirect(url_for('home.public.index')))
    set_access_cookies(response, "")
    set_refresh_cookies(response, "")
    return response

def register():
    pass

def refresh():
    pass

def load_logged_in_user():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            user = Repository.get_user_by_id(int(user_id))
            return {'current_user': user}
    except Exception:
        pass

    return {'current_user': None}
