from django.http import HttpResponse
from django.contrib.auth import authenticate

import json
import uuid

from errormessages import *
from models import *

SETTING_DATEFORMAT = "%d.%m.%Y %H:%M"


def error(errormessage=ERROR_UNKNOWN):
    """
        returns a dict with error status together with
            a message describing the error.
        @param errormessage: String describing the error.
            (will be displayed in the client)
    """
    return HttpResponse(json.dumps({
        "status": "error",
        "errormessage": errormessage,
    }))


def success(data={}):
    """
        returns a  dict with success status together with
            data from the {data} parameter which will be added to the dict.
        @param data: dict with data, which will be sent to the client.
    """
    response_dict = {"status": "success"}
    response_dict.update(data)
    return HttpResponse(
        json.dumps(response_dict)  # add the data dict
    )


def api(request):
    """
        API view, which reads the GET-Parameters and uses the
            the right view function and returns its result.
    """
    GET = request.GET
    token = None

    # check parameters
    if "tokenrequest" in GET:
        return api_tokenrequest(request)
    elif not "token" in GET:
        return error(ERROR_NO_TOKEN_GIVEN)

    # get the token
    try:
        token = Token.objects.get(token=GET.get("token"))
    except Device.DoesNotExist:
        return error(ERROR_TOKEN_DOES_NOT_EXIST)  # XXX: DEVICE_DOES_NOT_EXIST?
    except Token.DoesNotExist:
        return error(ERROR_TOKEN_DOES_NOT_EXIST)
    if not token.is_active:
        return error(ERROR_TOKEN_DISABLED)

    token.save()  # update last_used

    if "add" in GET:
        return api_add(request, token, GET.get("url", ""))
    elif "delete" in GET:
        return api_delete(request, token, GET.get("id", ""))

    return api_geturls(request, token)


def api_tokenrequest(request):
    """
        view to process a token request.
        The needed parameters in request.GET are:
        - user: the username, the token is requested for
        - device: the device name, the token is requested for.
            non-existant devices will be created by the token request.
        - password: the user password, to authenticate the request.
        on success, the view returns a unique token to the client,
        which can be used to access the other api functions.
    """
    GET = request.GET
    user = None  # user as User instance
    device = None  # device as String

    # check parameters
    if not "user" in GET:
        return error(ERROR_NO_USER_GIVEN)
    if not "password" in GET:
        return error(ERROR_NO_PASSWORD_GIVEN)
    elif not "device" in GET:
        return error(ERROR_NO_DEVICE_GIVEN)

    # get User
    user = authenticate(
        username=GET.get("user", ""),
        password=GET.get("password", "")
    )
    if user is None:
        return error(ERROR_USERNAME_OR_PASSWORD_WRONG)

    # get or create Device
    devicename = GET.get("device")
    try:
        device = Device.objects.get(name=devicename)
    except Device.DoesNotExist:
        device = Device(user=user, name=devicename)
        device.save()

    # create token
    token = Token(user=user, device=device, token=str(uuid.uuid4()))
    token.save()

    return success({
        "token": token.token
    })


def api_geturls(request, token):
    """
        view to return the urllists to a client.
        @param token: the client token
        returns either success with a dict of devices mapping
        to urllists, or error because of invalid or inactive tokens.
    """
    device = token.device
    user = token.user
    hosts_list = []

    for device in user.device_set.all():
        urls = []
        for url in device.url_set.all().order_by("created"):
            urls.append({
                "id": url.id,
                "link": url.content,
                "created": url.created.strftime(SETTING_DATEFORMAT),
            })
        hosts_list.append({
            "hostname": device.name,
            "urls": urls
        })
    return success({
        "hosts": hosts_list,
    })


def api_add(request, token, url):
    """
        view to add an url to a urllist. The device of the urllist,
        where the url will be added to is given by token.device.
        @param token: the client token
        @param url: the url to add.
    """
    if url == "":
        return error(ERROR_EMPTY_URL)
    else:
        user = token.user
        device = token.device
        Url(user=user, device=device, content=url).save()
        return success()


def api_delete(request, token, url_id):
    """
        view to delete an url from a urllist.
        @param token: the client token
        @param url_id: a unique id of the url,
            as returned by the urllist response.
    """
    try:
        Url.objects.get(id=url_id).delete()
        return success()
    except Url.DoesNotExist:
        return error(ERROR_URL_DOES_NOT_EXIST)
