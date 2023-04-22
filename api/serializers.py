from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions

from .models import TokenUsage

from api.utilities.authenticate import get_user


class EmailAuthTokenSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:

            user = get_user(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)

        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data


class DeveloperRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)


class TokenUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUsage
        fields = ['id', 'user', 'timestamp', 'prompt_tokens_used',
                  'completion_tokens_used', 'total_tokens_used']
        read_only_fields = ['id', 'user', 'timestamp']


class TextSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=10, max_length=500)
