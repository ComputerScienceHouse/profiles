import os
import subprocess
import requests
import csh_ldap

import flask_migrate
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

auth = OIDCAuthentication(app, issuer=app.config["OIDC_ISSUER"],
                          client_registration_info=app.config["OIDC_CLIENT_CONFIG"])


# LDAP
_ldap = csh_ldap.CSHLDAP(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'])

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# Import ldap model after instantiating object
# pylint: disable=wrong-import-position
from profiles.utils import before_request, get_member_info, process_image
from profiles.ldap import(ldap_update_profile,
                                        get_image,
                                        ldap_get_active_members,
                                        ldap_get_all_members,
                                        ldap_get_member,
                                        ldap_search_members,
                                        ldap_is_active,
                                        ldap_get_eboard,
                                        _ldap_get_group_members,
                                        ldap_get_group_desc,
                                        ldap_get_year)


@app.route("/", methods=["GET"])
@auth.oidc_auth
@before_request
def home(info=None):
    return redirect("/user/" + info["uid"], code=302)


@app.route("/user/<uid>", methods=["GET"])
@auth.oidc_auth
@before_request
def user(uid=None, info=None):
    return render_template("profile.html",
    						  info=info,
    						  member_info=get_member_info(uid))


@app.route("/results", methods=["POST"])
@auth.oidc_auth
@before_request
def results():
    searched = request.form['query']
    return redirect("/search/{}".format(searched), 302)


@app.route("/search", methods=["GET"])
@auth.oidc_auth
@before_request
def search(searched=None, info=None):
    # return jsonify(ldap_search_members(searched))
    searched = request.args.get("q")
    return render_template("listing.html",
    						  info=info,
    						  title="Search Results: "+searched,
    						  members=ldap_search_members(searched))


@app.route("/group/<_group>", methods=["GET"])
@auth.oidc_auth
@before_request
def group(_group=None, info=None):
    group_desc = ldap_get_group_desc(_group)

    if _group == "eboard":
        return render_template("listing.html",
    						    info=info,
    						    title=group_desc,
    						    members=ldap_get_eboard())

    return render_template("listing.html",
    						    info=info,
    						    title=group_desc,
    						    members=_ldap_get_group_members(_group))


@app.route("/year/<_year>", methods=["GET"])
@auth.oidc_auth
@before_request
def year(_year=None, info=None):
    return render_template("listing.html",
                                     info=info,
                                     title="Year: "+_year,
                                     members=ldap_get_year(_year))


@app.route("/update", methods=["POST"])
@auth.oidc_auth
@before_request
def update(info=None):
    if 'photo' in request.form:
        process_image(request.form['photo'][22:], info['uid'])
        get_image.cache_clear()

    ldap_update_profile(request.json, info['uid'])
    return jsonify({"success": True}), 200


@app.route('/upload', methods=['POST'])
@auth.oidc_auth
@before_request
def upload(info=None):
    if 'photo' in request.form:
        process_image(request.form['photo'][22:], info['uid'])
        get_image.cache_clear()
    return redirect('/', 302)


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("/", 302)


@app.route("/image/<uid>", methods=["GET"])
def image(uid):
    return get_image(uid)
