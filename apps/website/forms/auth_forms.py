from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Override User model
        model = get_user_model()
