# django-sharedurllist
## What is the sharedUrlList django-app?
The sharedUrlList django-app is a server implementation for sharing URLs across multiple devices.
Urls can be added, deleted and from different devices, and are listed seperated by device, from which the url was added.
The app can be used either by the Bookmarklets, which can be created in the webinterface, or with clients, which use the API, like the SharedUrlList android app.

## Requirements
The app needs the following python packages:

* django==1.5.1
* django-jquery==1.9.1

## Installation
### settings.py
* add "sharedurllist to your INSTALLED_APPS
* add "jquery" to your INSTALLED_APPS
* add [the default TEMPLATE\_CONTEXT\_PROCESSORS](https://docs.djangoproject.com/en/1.5/ref/settings/\#std:setting-TEMPLATE_CONTEXT_PROCESSORS) list.
* add "sharedurllist.context\_processors.devices" to the TEMPLATE\_CONTEXT\_PROCESSORS list.
* enable the django.contrib.staticfiles App, configure the folders and run "manage.py collectstatic"
* create an admin user and add all users, which should use it, as there is not registration, yet.

### urls.py
* add an include('sharedUrlList.urls') url to your urlpatterns.

## Building
* download bootstrap to "sharedurllist/static/bootstrap/"
* use setup.py to install or create distribution files
