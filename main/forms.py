from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import formmodel
from captcha.fields import CaptchaField
class FormModelForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = formmodel
        fields = ['first_name', 'last_name', 'email', 'message']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        EmailValidator()(email)  # Validates email format
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').strip()
        if not first_name.replace(' ', '').isalpha():
            raise ValidationError("First name should only contain letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip()
        if not last_name.replace(' ', '').isalpha():
            raise ValidationError("Last name should only contain letters.")
        return last_name

    def clean_message(self):
        message = self.cleaned_data.get('message').strip()
        # Additional security checks can be implemented here if needed
        return message

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation that involves multiple fields
        return cleaned_data
