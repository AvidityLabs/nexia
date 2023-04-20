# serializers.py
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User, Prompt, UseCase, Tone, AIModel, TokenUsage, PromptCategory



class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError(_('Invalid email or password'))
            if not user.is_active:
                raise serializers.ValidationError(_('User account is disabled.'))
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(_('Must include "email" and "password".'))
class ObtainEmailAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = ['id']


class DeveloperRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)


class UseCaseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = UseCase
        fields = ['id', 'name', 'description']

class ToneSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Tone
        fields = ['id', 'name']


class PromptSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    prompt = serializers.CharField(read_only=True)

    class Meta:
        model = Prompt
        fields = ['id', 'description', 'usecase', 'nov', 'tone', 'prompt']

class TokenUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUsage
        fields = ['id', 'user', 'timestamp', 'prompt_tokens_used', 'completion_tokens_used', 'total_tokens_used']
        read_only_fields = ['id', 'user', 'timestamp']


class CreateEditSerializer(serializers.Serializer):
    input = serializers.CharField(required=False, allow_blank=True)
    usecase = serializers.IntegerField()
    model = serializers.CharField()
    
class CompletionSerializer(serializers.Serializer):
    model = serializers.CharField()
    prompt = serializers.CharField(required=False, allow_blank=True)
    max_tokens = serializers.IntegerField()
    temperature = serializers.FloatField()
    top_p = serializers.FloatField()
    n = serializers.IntegerField()
    stream = serializers.BooleanField()
    logprobs = serializers.IntegerField(required=False, allow_null=True)
    stop = serializers.CharField(required=False, allow_blank=True)
    useSavedPrompt = serializers.BooleanField(required=True)
    promptId = serializers.IntegerField(required=False)


class PromptCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptCategory

        fields = ['id', 'name']
        read_only_fields = ['id']