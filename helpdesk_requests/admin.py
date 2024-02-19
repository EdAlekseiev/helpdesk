from django.contrib import admin

from helpdesk_requests.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass
