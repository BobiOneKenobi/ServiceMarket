from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import ProfileEditForm, UserRegisterForm
from .models import Profile

class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("home")
    success_message = "Your account was created successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile-detail")
    success_message = "Your profile was updated successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.profile