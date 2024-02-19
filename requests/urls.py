from django.urls import path, include

from rest_framework import routers

from requests import views

router = routers.SimpleRouter()
router.register("clients", views.ClientRequestViewSet)
router.register("operators", views.OperatorRequestViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "requests"
