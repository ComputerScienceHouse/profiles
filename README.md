CSH Profiles
========

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
redirect you (HTTP 302) to gravatar or twitter using their CSH email. This will return
a default profile picture if there is no LDAP image or gravatar image associated
with the user's CSH account.

Authorization
-------------

Authentication happens via pyOIDC with CSH SSO, authenticating
as the user who is viewing the page. This makes it show that they can only 
view / modify attributes that they have access to.


The server uses heavy caching via lru_cache to speed up the results as much as possible.
