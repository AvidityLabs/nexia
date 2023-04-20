# serializers.py
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Prompt, UseCase, Tone, AIModel, TokenUsage, PromptCategory



class EmailAuthTokenSerializer(AuthTokenSerializer):
    username_field = 'email'

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