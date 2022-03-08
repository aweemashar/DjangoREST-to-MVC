from django.urls import include, path, re_path
from rest_framework import routers
from django.contrib import admin

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('drf_alchemy_app.urls')),
]
