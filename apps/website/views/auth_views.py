from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from apps.website.forms.auth_forms import SignUpForm
from apps.website.utils import validate_recaptcha_token


class SignInView(LoginView):
    # override redirect if user is logged
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ! ---- Google Services  ----
        context["g_recaptcha_publickey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form):
        if settings.DEBUG:
            return super().form_valid(form)
        # * ---- reCaptcha validation ----
        recaptcha_token: str = self.request.POST.get("g-recaptcha-response")
        success, score = validate_recaptcha_token(recaptcha_token)
        if success and score >= settings.RECAPTCHA_REQUIRED_SCORE:
            # On form and reCaptcha valid, log the user in
            return super().form_valid(form)
        # ! If reCaptcha not valid, return a non field error
        form.add_error(None, "Invalid reCaptcha, please try again.")
        return super().form_invalid(form)


class SignOutView(LogoutView):
    pass


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("website:login")
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ! ---- Google Services  ----
        context["g_recaptcha_publickey"] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form):
        if settings.DEBUG:
            return super().form_valid(form)
        # * ---- reCaptcha validation on production ----
        recaptcha_token: str = self.request.POST.get("g-recaptcha-response")
        success, score = validate_recaptcha_token(recaptcha_token)
        if success and score >= settings.RECAPTCHA_REQUIRED_SCORE:
            # On form and reCaptcha valid, create user
            form.save()
            return super().form_valid(form)
        # ! If reCaptcha not valid, return a non field error
        form.add_error(None, "Invalid reCaptcha, please try again.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse("website:homepage"))
        return super().get(request, *args, **kwargs)
