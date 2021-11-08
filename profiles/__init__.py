import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.exc import SQLAlchemyError
import ldap
import csh_ldap
from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

auth = OIDCAuthentication(app, issuer=app.config["OIDC_ISSUER"],
                          client_registration_info=app.config["OIDC_CLIENT_CONFIG"])

# Sentry
# pylint: disable=abstract-class-instantiated
sentry_sdk.init(
    dsn=app.config['SENTRY_DSN'],
    integrations=[FlaskIntegration(), SqlalchemyIntegration()]
)

# LDAP
_ldap = csh_ldap.CSHLDAP(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'])

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# Import ldap model after instantiating object
# pylint: disable=wrong-import-position
from profiles.utils import before_request, get_member_info, process_image
from profiles.ldap import(ldap_update_profile,
                                        ldap_get_member,
                                        ldap_is_active,
                                        _ldap_get_group_members,
                                        ldap_get_active_members,
                                        ldap_get_intro_members,
                                        ldap_get_onfloor_members,
                                        ldap_get_current_students,
                                        ldap_get_all_members,
                                        ldap_get_groups,
                                        ldap_get_group_desc,
                                        ldap_get_eboard,
                                        ldap_search_members,
                                        ldap_get_year,
                                        ldap_is_rtp,
                                        get_image,
                                        get_gravatar,
                                        proxy_image,
                                        BadQueryError)


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
    return redirect(f"/search/{searched}", 302)


@app.route("/search", methods=["GET"])
@auth.oidc_auth
@before_request
def search(searched=None, info=None):
    # return jsonify(ldap_search_members(searched))
    searched = request.args.get("q")
    members = ldap_search_members(searched)
    if len(members) == 1:
        return redirect("/user/" + members[0].uid, 302)
    return render_template("listing.html",
    						  info=info,
    						  title="Search Results: "+searched,
    						  members=members)


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


@app.route('/clearcache')
@auth.oidc_auth
@before_request
def clear_cache(info=None):
    if not ldap_is_rtp(info['user_obj']):
        return redirect("/")

    ldap_get_active_members.cache_clear()
    ldap_get_intro_members.cache_clear()
    ldap_get_onfloor_members.cache_clear()
    ldap_get_current_students.cache_clear()
    ldap_get_all_members.cache_clear()
    ldap_get_groups.cache_clear()
    ldap_get_group_desc.cache_clear()
    ldap_get_eboard.cache_clear()
    ldap_search_members.cache_clear()
    ldap_get_year.cache_clear()
    get_image.cache_clear()
    get_gravatar.cache_clear()
    proxy_image.cache_clear()

    flash('Cache cleared!')

    return redirect(request.referrer, 302)


@app.errorhandler(404)
@app.errorhandler(500)
def handle_internal_error(e):
    if isinstance(e.original_exception, BadQueryError):
        return render_template("404.html", message=e.original_exception), 404
    raise e.original_exception


@app.route('/api/v1/healthcheck', methods=["GET"])
def health_check():
    #   Return codes
    #       200 - Success
    #       512 - LDAP failure
    return_code = 200
    jsonout = {
        "ldap": {
            "status": True,
            "server": None,
        }
    }
    try:
        jsonout["ldap"]["server"] = _ldap.server_uri
        ldap_get_active_members()
    except ldap.LDAPError:
        jsonout["ldap"]["status"] = False
        return_code = 512

    return jsonify(jsonout), return_code
