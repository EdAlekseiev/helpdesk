from django.contrib import admin

from requests.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass
