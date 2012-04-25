shim.twitter
============

Dataware shim Horizon

====
Developer environment: 
  1. server: Django + Sqlite3 
    1.1. Sqlite3 can change to other database, as it is supported in Django db backend
    1.2. Django server can also modify into Google App Engine with little change on NoSql: check https://developers.google.com/appengine/articles/django-nonrel
  2. python dependencies (non-core to python 2.7): 
    2.1: httplib2: http://code.google.com/p/httplib2/
    2.2: python-oauth2: https://github.com/simplegeo/python-oauth2

====
git sync:
  1. git clone git@github.com:jianhuashao/shim.twitter.git
  2. git checkout
  3. git submodule init : run this code to have submodule synchronised, otherwise submodule may just be a empty directory. 
  4. git submodule update
  5. git pull
  
====
run from command:
  1. cd django/s_twitter
  2. python manage.py syncdb : init the database, it is sqlite3 here in development.
  3. python manage.py runserver 0.0.0.0:8080 : to support all network interface, so use 0.0.0.0, otherwise, it may not be able to access through LAN.
  4. ipconfig or ifconfig : find out the network ip, for example, 128.243.35.212 
  5. use web broswer to visit http://128.23.35.212:8080


====
start catalog:
  1. code: https://github.com/jog/dataware.catalog
  2. make sure the user can be found in AuthorizationModule.py in function 'resource_authorize()'. you may have to create a a user in mysql first, and manully add it.
  3. change the server port into 8090 in CatalogServer.py
  4. start by: python CatalogServer.py
test catalog in shim:
  1. cd shim.django.s_twiter/catalog
  2. python catalog_resource_access_test.py




