from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from apps.website.forms.auth_forms import SignUpForm


class SignInView(LoginView):
    # override redirect if user is logged
    redirect_authenticated_user = True


class SignOutView(LogoutView):
    pass


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("website:login")
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse("website:homepage"))
        return super().get(request, *args, **kwargs)
