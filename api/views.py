import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import TextToImage, TextToVideo
from .serializers import TextToImageSerializer, TextToVideoSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from api.renderers import UserJSONRenderer
from api.utilities.hugging_face.queries import query_emotions_model, query_sentiment_model
from api.utilities.hugging_face.utils  import rename_sentiment_labels, add_emotion_percentages
from api.utilities.tokens import update_token_usage
from api.utilities.openai.utils import completion
from api.utilities.hugging_face.tokenizer import calculate_tokens

from api.serializers import (
    DeveloperRegisterSerializer,
    TextSerializer,
    LoginSerializer,
    UserSerializer,
    TextToImageSerializer,
    TextToVideoSerializer
)


logger = logging.getLogger(__name__)
ERROR_MSG = 'Oops, something went wrong. If this issue persists, please contact our customer support team at aviditylabs@hotmail.com for assistance. We apologize for the inconvenience and appreciate your patience as we work to resolve the issue.'
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
        # handles everything we need
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
                    return Response({'error': f'{ERROR_MSG}'}, status=400)

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
                return Response({'error': f'{ERROR_MSG}'}, status=400)
        else:
            logger.error(f"An error occurred @api/emotion_analysis/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)

class TextSentimentAnalysisView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_sentiment_model(text)
                if response_data is None:
                    return Response({"error":ERROR_MSG}, status=400)

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
        

class ChatGPTCompletionView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_sentiment_model(text)
                if response_data is None:
                    return Response({'error': f'{ERROR_MSG}'}, status=400)

                response = completion(text)
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage 
                update_token_usage(user, prompt_tokens, completion_tokens, total_tokens)
                result = {
                    "result": response.choices[0].message,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                logger.error(f"An error occurred @api/gpt/completion/: {e}")
                return Response({'error': f'{ERROR_MSG}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(text_serializer.errors)
            logger.exception(f"An error occurred @api/gpt/completion/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)
        

class GenerateImageView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_sentiment_model(text)
                if response_data is None:
                    return Response({'error': f'{ERROR_MSG}'}, status=400)

                response = completion(text)
                prompt_tokens = response.completion.usage.prompt_tokens
                completion_tokens = response.completion.usage.completion_tokens
                total_tokens = response.completion.usage.total_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage 
                update_token_usage(user, prompt_tokens, completion_tokens, total_tokens,img_count=1)
                result = {
                    "result": response.imgUrl,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                print(e)
                logger.error(f"An error occurred @api/generate/img: {e}")
                return Response({'error': f'{ERROR_MSG}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.exception(f"An error occurred @api/generate/img{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)
        

class TextToImageView(generics.CreateAPIView):
    queryset = TextToImage.objects.all()
    serializer_class = TextToImageSerializer

    def create(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        if text:
            # Generate the image based on the input text
            text_to_image = TextToImage.objects.create()
            text_to_image.generate_image(text)
            serializer = TextToImageSerializer(text_to_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Please provide input text'}, status=status.HTTP_400_BAD_REQUEST)

class TextToVideoView(generics.CreateAPIView):
    queryset = TextToVideo.objects.all()
    serializer_class = TextToVideoSerializer

    def create(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        if text:
            # Generate the video based on the input text
            text_to_video = TextToVideo.objects.create()
            text_to_video.generate_video(text)
            serializer = TextToVideoSerializer(text_to_video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Please provide input text'}, status=status.HTTP_400_BAD_REQUEST)
