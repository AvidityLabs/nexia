import logging
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from api.utilities.validators.text_validator import validate_text_input
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from api.utilities.tokens import MonthlyTokenLimitExceeded
from api.utilities.tokens import validate_token_usage
from api.renderers import APIJSONRenderer
from .models import Draft, Instruction, PricingPlan, TextToImage, TextToVideo, TokenUsage, Tone, UseCase, User
from .serializers import  DraftSerializer, InstructionSerializer, InstructionSerializerResult, TextCompletionSerializer, TextToImageSerializer, TextToVideoSerializer, ToneSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from api.renderers import UserJSONRenderer
from api.utilities.hugging_face.queries import query_emotions_model, query_sentiment_model
from api.utilities.hugging_face.utils import rename_sentiment_labels, add_emotion_percentages
from api.utilities.tokens import update_token_usage
from api.utilities.openai.utils import completion, edit
from api.utilities.hugging_face.tokenizer import calculate_tokens
from api.utilities.jwt_helper import decode_jwt_token
from api.utilities.data import TONES

from django.contrib.auth.models import (Group)

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

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    A view that provides retrieve and update capabilities for a user model.
    To retrieve user data, use GET method, and to update user data, use PUT or PATCH method.

    To retrieve user data:
        - You must be authenticated.
        - Endpoint: users/detail/<int:pk>/

    To update user data:
        - You must be authenticated.
        - Endpoint: users/detail/<int:pk>/
        - Data: {"user": {... updated user data ...}}

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (APIJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve and return the current authenticated user's data
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update and return the current authenticated user's data
        """
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "password": request.data.get('password')
        }
        try:
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            # Update subscription if the user is a rapid api user 
            user = get_object_or_404(User.objects.select_related('subscription__pricing_plan'), email=user['email'])
            subscription_meta = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
            # Subscription UPDATE only for RAPID API users 
            if subscription_meta and not user.is_app_user and user.subscription.pricing_plan.name != subscription_meta:
                pricing_plan, _ = PricingPlan.objects.get_or_create(name=subscription_meta)
                user.subscription.pricing_plan = pricing_plan
                user.subscription.save()
                # Update token usage 
                today = date.today()
                token_usage = TokenUsage.objects.filter(
                        user=user,
                        month=today.month,
                        year=today.year,
                    ).first()
                
                if token_usage:
                    token_usage.pricing_plan = pricing_plan
                    token_usage.save()
                else:
                    token_usage = TokenUsage(
                        user=user,
                        month=today.month,
                        year=today.year,
                        pricing_plan=pricing_plan,
                    )
                    token_usage.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class DeveloperRegisterView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = DeveloperRegisterSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "username": request.data.get('email'),
            "password": request.data.get('password'),
            "groups": [{'name':'developer'}]
        }

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Update subscription if the user is a rapid api user 
        data = {"email": serializer.data.get('email'), "token": serializer.data.get('token')}
        return Response(data, status=status.HTTP_201_CREATED)


class AppUserRegisterView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    renderer_classes = (APIJSONRenderer,)
    serializer_class = DeveloperRegisterSerializer

    def post(self, request):
        decoded_user_id = decode_jwt_token(request)
        if request.user.id == decoded_user_id:
            user = {
                "email": request.data.get('email'),
                "username": request.data.get('username'),
                "password": request.data.get('password'),
                "groups": request.data.get('groups'),
                "app_owner_id": request.user.id
            }

            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(str(request.user.id), status=status.HTTP_201_CREATED)
            # The user in the request is not the same as the user in the token
        return Response({'error': 'Invalid token for this user'}, status=401)


class TextEmotionAnalysisView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def post(self, request, format=None):
        text_serializer = TextCompletionSerializer(data=request.data)
        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_emotions_model(text)
                if response_data is None:
                    return Response({'error': f'{ERROR_MSG}|>>Detail: Unable to communicate with gpt model'}, status=400)

                data = add_emotion_percentages(response_data)
                # prepare_to_cal_token
                # Flatten the list of labels into a single list of labels
                flat_labels = [item["label"]
                               for sublist in data for item in sublist]
                flat_scores = [str(item["score"])
                               for sublist in data for item in sublist]
                flat_percentages = [str(item["percentage"])
                                    for sublist in data for item in sublist]
                # Convert the flat list of labels into a string
                string_response_data = "{}{}{}".format(" ".join(flat_labels), " ".join(
                    flat_percentages), " ".join(map(str, flat_scores)))

                prompt_tokens = calculate_tokens(text)
                completion_tokens = calculate_tokens(string_response_data)
                total_tokens = prompt_tokens + completion_tokens

                # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage
                update_token_usage(user, prompt_tokens,
                                   completion_tokens, total_tokens)
                result = {
                    "analysis": data,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                logger.exception(
                    f"An error occurred @api/emotion_analysis/: {e}")
                return Response({'error': f'{ERROR_MSG}|>>Detail: Unable to communicate with gpt model'}, status=400)
        else:
            logger.error(
                f"An error occurred @api/emotion_analysis/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)


class TextSentimentAnalysisView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def post(self, request, format=None):
        text_serializer = TextCompletionSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_sentiment_model(text)
                if response_data is None:
                    return Response({"error": f'{ERROR_MSG}|>>Detail: Unable to communicate with gpt model'}, status=400)

                fixed_labels = rename_sentiment_labels(response_data)
                fixed_labels_str = ''
                fixed_labels_str = "\n".join(
                    [f"{key}: {value}" for sublist in fixed_labels for dictionary in sublist for key, value in dictionary.items()])

                prompt_tokens = calculate_tokens(text)
                completion_tokens = calculate_tokens(fixed_labels_str)
                total_tokens = prompt_tokens + completion_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage
                update_token_usage(user, prompt_tokens,
                                   completion_tokens, total_tokens)
                result = {
                    "analysis": fixed_labels,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens_used": total_tokens,
                }
                return Response(data=result, status=200)
            except Exception as e:
                print(e)
                logger.error(
                    f"An error occurred @api/sentiment_analysis/: {e}")
                return Response({'error': f'{ERROR_MSG}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(text_serializer.errors)
            logger.exception(
                f"An error occurred @api/sentiment_analysis/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)


class ChatGPTCompletionView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def post(self, request, format=None):

        validate_token_usage(request.user)

        text_serializer = TextCompletionSerializer(data=request.data)

        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response = completion(request.data.get('text'))
                if response is None:
                    return Response({'error': f'{ERROR_MSG}|>>Detail: Unable to communicate with gpt model'}, status=400)

                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage
                update_token_usage(user, prompt_tokens,
                                   completion_tokens, total_tokens)
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
            logger.exception(
                f"An error occurred @api/gpt/completion/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)

class ChatGPTEditView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def post(self, request, format=None):

        validate_token_usage(self.request.user)

        text_serializer = TextSerializer(data=request.data)
        if text_serializer.is_valid():
            text = request.data.get('text')
            instruction = request.data.get('instruction')
            try:
                response = edit(text,instruction)
                if response is None:
                    return Response({'error': f'{ERROR_MSG}'}, status=400)

                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                # # # Track token usage
                user = request.user
                # Assuming user and num_tokens are defined update token usage
                update_token_usage(user, prompt_tokens,
                                   completion_tokens, total_tokens)

                return Response(data=response, status=200)
            except Exception as e:
                logger.error(f"An error occurred @api/prompt/edit/: {e}")
                return Response({'error': f'{ERROR_MSG}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.exception(
                f"An error occurred @api/prompt/edit/{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)

class GenerateImageView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

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
                update_token_usage(user, prompt_tokens,
                                   completion_tokens, total_tokens, img_count=1)
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
            logger.exception(
                f"An error occurred @api/generate/img{text_serializer.errors}")
            return Response({'error': text_serializer.errors}, status=400)


class TextToImageView(generics.CreateAPIView):
    queryset = TextToImage.objects.all()
    serializer_class = TextToImageSerializer
    renderer_classes = (APIJSONRenderer,)

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
    renderer_classes = (APIJSONRenderer,)

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


class CreateToneAPIView(APIView):
    renderer_classes = (APIJSONRenderer,)
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Tone detail required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the 'name' field
        is_valid, error_msg = validate_text_input(name)
        if not is_valid:
            return Response({'error': f'Invalid tone. {error_msg}'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the 'name' field already exists in the database
        if Tone.objects.filter(name__iexact=name, created_by=self.request.user.id).exists():
            return Response({'error': 'Tone with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = Tone.objects.create(
                created_by=request.user.id,
                name=name
            )
            serializer = ToneSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ToneListView(generics.ListAPIView):
    serializer_class = ToneSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)


    def get_queryset(self):
        queryset = Tone.objects.filter(created_by=self.request.user.id)
        # Instruction.objects.filter(user_id=self.request.user.id)
        # Get the search query parameter from the request
        search_query = self.request.query_params.get('q')
        # If the search query is present, filter the queryset by the name field
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ToneRetrieveView(generics.RetrieveAPIView):
    serializer_class = ToneSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        return Tone.objects.filter(created_by=self.request.user.id)

class ToneUpdateView(generics.RetrieveAPIView):
    serializer_class = ToneSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        return Tone.objects.filter(created_by=self.request.user.id)

class InstructionCreateView(APIView):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        # Get data from request
        description = request.data.get('description')
        tones_data = self.request.data.get('tones')
        audience = self.request.data.get('audience')
        style = self.request.data.get('style')
        context = self.request.data.get('context')
        language = self.request.data.get('language')
        length = self.request.data.get('length')
        source_text = self.request.data.get('source_text')
        is_desc_valid = validate_text_input(text=description)

        # Validate data
        is_desc_valid = validate_text_input(text=description)
        if is_desc_valid[0] == False:
            return Response({'error': f'Description is required. {is_desc_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        if not tones_data:
            return Response({'error': 'At least one tone is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate audience
        is_audience_valid = validate_text_input(text=audience)
        if audience and is_audience_valid[0] == False:
            return Response({'error': f'Audience {is_audience_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate style
        is_style_valid = validate_text_input(text=style)
        if style and is_style_valid[0] == False:
            return Response({'error': f'Style {is_style_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate context
        is_context_valid = validate_text_input(text=context)
        if context and is_context_valid[0] == False:
            return Response({'error': f'Context {is_context_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate language
        is_language_valid = validate_text_input(text=language)
        if language and is_language_valid[0] == False:
            return Response({'error': f'Language {is_language_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate length
        is_length_valid = validate_text_input(text=length)
        if length and is_length_valid[0] == False:
            return Response({'error': f'Length {is_length_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate source text
        is_source_text_valid = validate_text_input(text=source_text)
        if source_text and is_source_text_valid[0] == False:
            return Response({'error': f'Source text {is_source_text_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if instruction with the same description already exists
        existing_inst = Instruction.objects.filter(description=description).first()
        if existing_inst:
            # If exists, return the existing instance
            serializer = InstructionSerializer(existing_inst)
            return Response({"message": "Instruction with the provided description already exists, returning existing instance","data":serializer.data }, status=status.HTTP_200_OK  )

        # Add tones to Instruction object
        tones = []
        for tone in tones_data:
            is_tone_valid = validate_text_input(tone)

            if is_tone_valid[0] == False:
                return Response({'error': f'At least one tone is required. {is_tone_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)

            tone, created = Tone.objects.get_or_create(name=tone)
            if created:
                tone.created_by = self.request.user.id
                tone.save()
            tones.append(tone)

        source_txt =  self.request.data.get('source_text')
        if not source_txt:
            source_txt=''
        inst_obj = Instruction.objects.create(
            description=description,
            created_by=request.user.id,
            audience = self.request.data.get('audience'),
            style = self.request.data.get('style'),
            context = self.request.data.get('context'),
            language = self.request.data.get('language'),
            length = self.request.data.get('length'),
            source_text = source_txt
        )
        inst_obj.tones.set(tones)
        inst_obj.save()
        serializer = InstructionSerializer(inst_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class InstructionRetrieveView(generics.RetrieveAPIView):
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        return Instruction.objects.filter(created_by=self.request.user.id)


class InstructionUpdateView(APIView):
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        return Instruction.objects.filter(created_by=self.request.user.id)

    def put(self, request, pk):
        try:
            instruction = self.get_queryset().get(pk=pk)
        except Instruction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if instruction.created_by != self.request.user.id:
            return Response({'error': 'You can only update the instructions you created.'},status=status.HTTP_403_FORBIDDEN)

        desc = request.data.get('description')
        tones = request.data.get('tones')
        

        if desc:
            instruction.description = desc

        if tones:
            tones_data = []
            for tone_item in tones:
                is_tone_valid = validate_text_input(text=tone_item)
                if is_tone_valid[0]==False:
                    return Response({'error': f'Invalid tone. {is_tone_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)
                tone, _ = Tone.objects.get_or_create(name=tone_item)
                if tone is None:
                    return Response({'error': f'Invalid tone: {tone_item}'}, status=status.HTTP_400_BAD_REQUEST)
                tones_data.append(tone)
            instruction.tones.set(tones_data)

        serializer = InstructionSerializerResult(instruction)
        return Response(serializer.data, status=status.HTTP_200_OK)
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class InstructionListView(generics.ListAPIView):
    serializer_class = InstructionSerializerResult
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        return Instruction.objects.filter(created_by=self.request.user.id)
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class InstructionSearchView(generics.ListAPIView):
    serializer_class = InstructionSerializerResult
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    def get_queryset(self):
        queryset = Instruction.objects.filter(created_by=self.request.user.id)
        description = self.request.query_params.get('description', None)
        tones = self.request.query_params.getlist('tones', [])

        if description is not None:
            queryset = queryset.filter(description__icontains=description)
        if tones:
            queryset = queryset.filter(tones__name__in=tones).distinct()
        return queryset

class DraftListCreateView(generics.ListCreateAPIView):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        use_case = request.data.get('use_case')
        title = request.data.get('title')
        content = request.data.get('content')

        use_case, _ = UseCase.objects.get_or_create(name=use_case)

        draft = Draft(user=user, use_case=use_case, title=title, content=content)
        draft.save()

        serializer = DraftSerializer(draft)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DraftRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer