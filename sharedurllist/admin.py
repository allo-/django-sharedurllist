from django.contrib import admin
from models import *


class UrlAdmin(admin.ModelAdmin):
    list_display = ("user", "device", "created", "content")
    list_filter = ("user", "device", "created")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    list_filter = ("user",)


def token_abbreviated(obj):
    return obj.token[0:9] + "..."
token_abbreviated.short_description = "Token"


class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "device", "created", "last_used",
                    "is_active", token_abbreviated)
    list_filter = ("user", "device", "last_used")
    readonly_fields = ("token",)
    list_editable = ("is_active",)

admin.site.register(Url, UrlAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Token, TokenAdmin)
