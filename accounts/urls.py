from django.urls import path
from .views import (
    ProfileDetailView,
    ProfileUpdateView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
]