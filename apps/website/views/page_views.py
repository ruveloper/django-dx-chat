from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "website/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
