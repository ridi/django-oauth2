Changelog
=========
1.0.1 (Oct 10st 2019)
------------------
- Change lib dir to ridi_django_oauth2_lib for preventing dir conflict
- Update README.md

1.0.0 (Oct 10st 2019)
------------------
- Change main logic to get public key from OAuth2 server
    - to get public key, it sends request to OAuth2 server, and memorize that key until key expires.
    - when getting public key, it use [JWKS](https://tools.ietf.org/html/rfc7517) type
    - it makes able to adapt OAuth2 server's key changing dynamically and using multi key.  

0.0.15 (Aug 1st 2019)
------------------
- Add cryptography in package  

0.0.12 (Apr 23th 2019)
------------------
- Support select jwt sign key by kid

0.0.11 (Apr 17th 2018)
------------------
- Change dependency version

0.0.10 (Apr 6th 2018)
------------------
- Add missing file for rest_framework
    - `__init__.py`

0.0.9 (Apr 6th 2018)
------------------
- Update requirements

0.0.8 (Apr 6th 2018)
------------------
- Support Django Rest Framework

0.0.7 (Apr 3th 2018)
------------------
- Change package name

0.0.6 (Apr 2nd 2018)
------------------
- Test travis deploy

0.0.5 (Mar 23th 2018)
------------------
- Remove `expire_margin`

0.0.4 (Mar 22nd 2018)
------------------
- Change primary field type in RidiUser
- Implement __str__ in RidiUser

0.0.3 (Mar 20th 2018)
------------------
- Rewrite code structure in ridi_oauth2 package.
    - Change grant object, change logic for check scope and ...etc
- Add migrations about RidiUser Model
- Configure travis

0.0.2 (Mar 16th 2018)
------------------
### Fix
- Fix login_required Decorator

0.0.1 (Mar 9th 2018)
------------------
### Register New Package
- Addition of initial functions related to OAuth2.
    - Pure Python Client
    - Django Binding
        - Django Binding Library reflected the policy of RIDI.
