"""
URL configuration for weather_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from weather import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("accounts/login/", views.user_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("weather/", views.weather_home, name="weather_home"),
    path("", views.weather_home, name="weather_home"),  # Default to weather homepage
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_otp_password/", views.verify_otp_password, name="verify_otp_password"),
    path("reset_password/", views.reset_password, name="reset_password"),
]
