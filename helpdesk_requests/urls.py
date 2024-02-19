from django.urls import path, include

from rest_framework import routers

from helpdesk_requests import views

router = routers.SimpleRouter()
router.register(
    "clients",
    views.ClientRequestViewSet,
    basename="request-clients",
)
router.register(
    "operators",
    views.OperatorRequestViewSet,
    basename="request-operators",
)

urlpatterns = [path("", include(router.urls))]

app_name = "helpdesk_requests"
