from rest_framework import serializers
from .models import UseCase

class EmailGenerationSerializer(serializers.Serializer):
    language = serializers.CharField()
    tone = serializers.CharField()
    email_content = serializers.CharField()
    
    

class UseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseCase
        fields = ('id', 'title', 'function_name', 'description', 'navigateTo', 'category')