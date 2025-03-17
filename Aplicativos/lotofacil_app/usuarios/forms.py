from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona help_text e mensagens personalizadas
        self.fields['password1'].help_text = "Sua senha deve conter pelo menos 8 caracteres, incluindo letras e números."
        self.fields['password2'].help_text = "Repita a senha para confirmação."

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email