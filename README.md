CSH Profiles
========

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

The Computer Science House @ RIT's web interface to our LDAP server containing
all of our members' data. Users are able to view other users information that
they have access to, modify their own data, and search through all users. You can
find users by going directly to their profile:
```html
<img src="https://profiles.csh.rit.edu/user/uid">
```

or via group pages:
```html
<img src="https://profiles.csh.rit.edu/group/gid">
```

or the site's built in search feature.

CSH Avatar
----------

Users can get the profile pictures of people by going to this url:
```html
<img src="https://profiles.csh.rit.edu/image/uid">
```

This will get the user's picture from LDAP or if they do not have one, will 
redirect you (HTTP 302) to gravatar using their CSH email. This will return
a default profile picture if there is no LDAP image or gravatar image associated
with the user's CSH account. If the user has their GitHub and/or Twitter attributes
set but has no LDAP image, their profile image from there will be proxied and served.

Authorization
-------------

Authentication happens via pyOIDC with CSH SSO, authenticating
as the user who is viewing the page. This makes it show that they can only 
view / modify attributes that they have access to.


The server uses heavy caching via lru_cache to speed up the results as much as possible.

Setup
-------------

Profiles has the following dependencies:

```
requests
csh_ldap==2.0.2
flask
flask_sqlalchemy
flask_migrate
flask-pyoidc
flask-optimize
PyMySQL
pyGravatar
Flask_Uploads
pylint
pillow
```
You can install them by running ```pip install -r requirements.txt``` in the program directory.

Create a copy of config.env.py named config.py and make the following modifications:

```
SERVER_NAME = os.environ.get('PROFILES_SERVER_NAME', 'profiles.csh.rit.edu')
``` 
to
```
SERVER_NAME = os.environ.get('PROFILES_SERVER_NAME', 'localhost:8080')
```

Reach out to an RTP to get OIDC credentials that will allow you to develop locally behind OIDC auth.

```LDAP_BIND_DN``` is your CSH DN. It is in the following format:

```uid={CSH User Name},cn=users,cn=accounts,dc=csh,dc=rit,dc=edu```


 ```LDAP_BIND_PASS``` is your CSH password.

 If you did everything right, you should be able to run ```python app.py``` and develop locally.


Code Standards
------------

Use Pylint to ensure your code follows standards. Commits will be pylinted by GitHub Actions, if your
build fails you must fix whatever it tells you is wrong before it will be merged.
