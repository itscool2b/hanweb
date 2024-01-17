from rest_framework import serializers
from django.core.validators import validate_email
from .models import formmodel

class FormModelSerializer(serializers.ModelSerializer):
    # Assuming captcha validation is handled separately as it's not a model field
    # captcha = serializers.CharField(write_only=True)

    class Meta:
        model = formmodel
        fields = ['first_name', 'last_name', 'email', 'message']

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_first_name(self, value):
        value = value.strip()
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("First name should only contain letters.")
        return value

    def validate_last_name(self, value):
        value = value.strip()
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Last name should only contain letters.")
        return value

    def validate_message(self, value):
        value = value.strip()
        # Additional security checks can be implemented here if needed
        return value


