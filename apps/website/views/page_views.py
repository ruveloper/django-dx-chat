from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "website/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Redirect to ChatPage if user is logged
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("website:chat"))
        return self.render_to_response(context)


class ChatPage(LoginRequiredMixin, TemplateView):
    template_name = "website/chat_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
