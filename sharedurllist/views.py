from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

import uuid

from models import *
from errormessages import *
from api import *


def get_device(user, devicename):
    """
        helper function to get or create a device for a given name
        @type user: User object
        @type devicename: String
    """
    try:
        device = Device.objects.get(name=devicename)
    except Device.DoesNotExist:
        device = Device(user=user, name=devicename)
        device.save()
    return device


def main(request):
    """
        main view, for the webinterface, as for the api,
            as the api uses only one url with GET-Parameters.
    """
    if "api" in request.GET:
        return api(request)
    else:
        return home(request)


def bookmarklet(request):
    """
        add a URL via bookmarklet, or list all bookmarklets of the user,
            when no url is given.
    """
    template_dict = {"view": "bookmarklet"}
    status = ""
    if len(request.GET) == 0:
        if not request.user.is_authenticated():
            return login_required(bookmarklet)(request)
        else:
            tokens = Token.objects.filter(user=request.user)
            if len(tokens) == 0:
                status = "You have not created any tokens, yet."
                template_dict["success"] = False
            template_dict["tokens"] = tokens
    else:
        try:
            token = Token.objects.get(token=request.GET.get("token"))
            if token.is_active:
                url = request.GET.get("url")
                if Url.objects.filter(user=token.user, device=token.device,
                                      content=url).count() > 0:
                    status = "Url already in list"
                else:
                    Url(user=token.user, device=token.device,
                        content=url).save()
                    status = "URL added."
                    template_dict['success'] = True
                    template_dict['url'] = url
                    template_dict['token'] = token
            else:
                template_dict['success'] = False
                status = "Token inactive"
        except Token.DoesNotExist:
            status = "invalid token."
            template_dict['success'] = False

    template_dict["status"] = status
    return render(request, "bookmarklet.html", template_dict)


@login_required
def home(request):
    """
        main view of the webinterface, listing devices with their urls
            and the token list.
    """
    return render(request, "home.html", {
        "view": "home",
        "tokens": Token.objects.filter(user=request.user),
        "devices": Device.objects.all(),
    })


@login_required
def delete_device(request):
    """
        delete device view
        needed POST-Parameters:
        - device_id with the id of the device.
            and redirects back to the main view.
    """
    if "device_id" in request.POST:
        try:
            Device.objects.get(id=request.POST.get("device_id", 0)).delete()
        except Device.DoesNotExist:
            pass
    return redirect(reverse(main))


def delete_url(request):
    """
        view for deleting an url
        needed POST-Parameters:

            redirects to main view with the current_tab
    """
    if "url" in request.POST:
        url = get_object_or_404(Url, id=request.POST.get("url"))
        url.delete()
    return redirect(reverse(main) + request.POST.get("current_tab", ""))


@login_required
def token(request):
    """
        creates, enables, disables or deletes a token
        needed POST-Parameters:
        - one of enable/disable/create/delete set
        - device: (only for create) devicename, to create the token for
        - token: (for all other calls) token to be enabled/disabled/deleted
        redirects to the main view, with the token-tab opened
    """
    POST = request.POST

    if POST.get("create") and POST.get("device"):
        device = get_device(request.user, POST.get("device"))
        Token(user=request.user, device=device, token=uuid.uuid4()).save()
    else:
        token = get_object_or_404(Token, token=POST.get("token"))

    if POST.get("disable"):
        token.is_active = False
        token.save()
    elif POST.get("enable"):
        token.is_active = True
        token.save()
    elif POST.get("delete"):
        token.delete()
    return redirect(reverse(main) + "#urltab_special-tokens")
