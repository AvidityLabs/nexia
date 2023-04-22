import re
from django.db.models import F
from api.utilities.transformers_tokenizer import calculate_tokens
from api.utilities.hugging_face import (
    query_emotions_model, query_sentiment_model)
from api.utilities.openai import *
from api.serializers import (
    DeveloperRegisterSerializer,
    EmailAuthTokenSerializer,
    TextSerializer,)
from api.models import (User, TokenUsage)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

# Validate prompt text length
MAX_PROMPT_LENGTH = 1000  # Maximum allowed length for prompt text


class ObtainEmailAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class DeveloperRegisterView(generics.CreateAPIView):
    serializer_class = DeveloperRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create(
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data['email'],
                    username=serializer.validated_data['email'],
                    is_developer=True
                )
                user.set_password(serializer.validated_data['password'])

                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    # Token already exists, delete the old one
                    token.delete()
                    # Create a new token
                    token = Token.objects.create(user=user)
                user.api_key = token.key
                user.save()

                return Response({'api_key': token.key}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextEmotionAnalysisView(APIView):
    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)

        if serializer.is_valid():
            text = serializer.validated_data['text']
            try:
                response_data = query_emotions_model(text)
                if response_data is None:
                    return Response('error', status=400)

                data = response_data[0]
                total_sum = sum(item['score'] for item in data)
                percentages = [(item['score'] / total_sum * 100) for item in data]
                for i, item in enumerate(data):
                    item['percentage'] = round(percentages[i], 2)

                cleaned_data = [re.sub("[^a-zA-Z0-9.]+", "", str(v)) for d in data for v in d.values()]
                r = "".join(cleaned_data)

                prompt_tokens = calculate_tokens(text)
                completion_tokens = calculate_tokens(r)
                total_tokens = prompt_tokens + completion_tokens

                # Track token usage
                user = request.user
                pricing_plan = user.subscription.pricing_plan
                prompt_tokens_used = response_data['usage'].get('prompt_tokens', 0)
                completion_tokens_used = response_data['usage'].get('completion_tokens', 0)
                total_tokens_used = response_data['usage'].get('total_tokens', 0)
                TokenUsage.objects.filter(
                    user=user,
                    pricing_plan=pricing_plan,
                ).update(
                    prompt_tokens_used=F('prompt_tokens_used') + prompt_tokens_used,
                    completion_tokens_used=F('completion_tokens_used') + completion_tokens_used,
                    total_tokens_used=F('total_tokens_used') + total_tokens_used,
                )

                result = {
                    "analysis": data,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                return Response({'error': 'An error occurred while processing your request. Please try again later.'}, status=400)
        else:
            error_message = "Invalid input data. Please ensure that the 'text' field is provided."
            return Response({'error': error_message, 'details': serializer.errors}, status=400)

