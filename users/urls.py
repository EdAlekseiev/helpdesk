from django.urls import path, include

from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register("clients", views.ClientViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "users"
