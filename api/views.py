import re

from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView

from api.serializers import LoginSerializer
from api.authentication.renderers import UserJSONRenderer
from api.utilities.transformers_tokenizer import calculate_tokens
from api.utilities.hugging_face import (
    query_emotions_model, query_sentiment_model)

from api.utilities.data_cleaning import rename_sentiment_labels, add_emotion_percentages
from api.utilities.validations import check_duplicate_email
from api.utilities.token_management import update_token_usage
from api.serializers import (
    DeveloperRegisterSerializer,
    TextSerializer,)
from api.models import (PricingPlan, User, TokenUsage)

import logging

from api.serializers import UserSerializer

logger = logging.getLogger(__name__)
ERROR_MSG='Something went wrong. If this issue persists please contact us through our customer support at aviditylabs@hotmail.com'
# Validate prompt text length
MAX_PROMPT_LENGTH = 1000  # Maximum allowed length for prompt text



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "password": request.data.get('password')
        }

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeveloperRegisterView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = DeveloperRegisterSerializer

    def post(self, request):

        user = {
            "email": request.data.get('email'),
            "username": request.data.get('username'),
            "password": request.data.get('password')
        }

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TextEmotionAnalysisView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)
        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_emotions_model(text)
                if response_data is None:
                    return Response({"error": "Failed to query AI model"}, status=400)

                data = add_emotion_percentages(response_data)
                #prepare_to_cal_token
                # Flatten the list of labels into a single list of labels
                flat_labels = [item["label"] for sublist in data for item in sublist]
                flat_scores = [str(item["score"]) for sublist in data for item in sublist]
                flat_percentages = [str(item["percentage"]) for sublist in data for item in sublist]
                # Convert the flat list of labels into a string
                string_response_data = "{}{}{}".format(" ".join(flat_labels), " ".join(flat_percentages), " ".join(map(str, flat_scores)))

                prompt_tokens = calculate_tokens(text)
                completion_tokens = calculate_tokens(string_response_data)
                total_tokens = prompt_tokens + completion_tokens

                # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage 
                update_token_usage(user, prompt_tokens, completion_tokens, total_tokens)
                result = {
                    "analysis": data,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                logger.exception(f"An error occurred @api/emotion_analysis/: {e}")
                return Response({'error': ERROR_MSG}, status=400)
        else:
            logger.error(f"An error occurred @api/emotion_analysis/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)

class TextSentimentAnalysisView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_sentiment_model(text)
                if response_data is None:
                    return Response('error', status=400)

                fixed_labels = rename_sentiment_labels(response_data)
                fixed_labels_str=''
                fixed_labels_str = "\n".join([f"{key}: {value}" for sublist in fixed_labels for dictionary in sublist for key, value in dictionary.items()])

                prompt_tokens = calculate_tokens(text)
                completion_tokens = calculate_tokens(fixed_labels_str)
                total_tokens = prompt_tokens + completion_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage 
                update_token_usage(user, prompt_tokens, completion_tokens, total_tokens)
                result = {
                    "analysis": fixed_labels,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                print(e)
                logger.error(f"An error occurred @api/sentiment_analysis/: {e}")
                return Response({'error': f'{ERROR_MSG}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(text_serializer.errors)
            logger.exception(f"An error occurred @api/sentiment_analysis/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)