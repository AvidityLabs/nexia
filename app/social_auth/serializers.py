from rest_framework import serializers

from social_auth.firebase import firebase_validation
from .register import register_social_user
import os
from decouple import config
from rest_framework.exceptions import AuthenticationFailed


class SocialAuthSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    photo_url = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    pricing_plan = serializers.CharField(write_only=True)
    auth_token = serializers.CharField(write_only=True)

    def validate(self, data):    
        token_str = self.initial_data.get('auth_token')
        plan = self.initial_data.get('pricing_plan')

        user_data = firebase_validation(token_str)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        aud = config('FIREBASE_CLIENT_ID')
        if user_data['aud'] != aud:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['display_name']
        provider = user_data['auth_provider']
        photo_url = user_data['photo_url']
        is_verified = user_data['is_verified']

        return register_social_user(provider=provider, user_id=user_id, email=email, display_name=name, pricing_plan=plan, photo_url=photo_url, is_verified=is_verified)
