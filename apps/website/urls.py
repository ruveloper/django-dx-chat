from django.urls import path

from apps.website.views.auth_views import SignInView, SignOutView, SignUpView
from apps.website.views.page_views import ChatPage, HomePage

app_name = "website"

urlpatterns = [
    # * ---- ACCOUNT URLS ----
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", SignOutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    # * ----- MAIN URLS ------
    path("", HomePage.as_view(), name="homepage"),
    path("chat/", ChatPage.as_view(), name="chat"),
]
