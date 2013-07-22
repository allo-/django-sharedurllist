from models import Device


def devices(request):
    if request.user.is_authenticated():
        return {
            "devices": Device.objects.filter(user=request.user)
        }
    else:
        return {}
