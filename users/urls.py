from django.urls import path, include

from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register("clients", views.ClientViewSet, basename="clients")
router.register("operators", views.OperatorViewSet, basename="operators")

urlpatterns = [path("", include(router.urls))]

app_name = "users"
