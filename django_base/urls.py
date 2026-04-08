"""
URL configuration for django_base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django_base.controller.user_controller import UserController

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/user/",
        UserController.as_view({"get": "list", "post": "create"}),
        name="api_user",
    ),
    path(
        "api/user/<int:pk>/",
        UserController.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="api_user_detail",
    ),
    path("silk/", include("silk.urls", namespace="silk")),
]
