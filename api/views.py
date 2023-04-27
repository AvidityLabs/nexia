import logging
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ValidationError
from api.utilities.validators.text_validator import validate_text_input
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Instruction, InstructionCategory, PricingPlan, Role, TextToImage, TextToVideo, TokenUsage, Tone, User
from .serializers import InstructionCategorySerializer, InstructionSerializer, InstructionSerializerResult, TextToImageSerializer, TextToVideoSerializer, ToneSerializer

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
from api.utilities.openai.utils import completion
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
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

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
    renderer_classes = (UserJSONRenderer,)
    serializer_class = DeveloperRegisterSerializer

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "username": request.data.get('username'),
            "password": request.data.get('password')
        }

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Update subscription if the user is a rapid api user 

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppUserRegisterView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
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

    def post(self, request, format=None):
        text_serializer = TextSerializer(data=request.data)
        if text_serializer.is_valid():
            text = text_serializer.validated_data['text']
            try:
                response_data = query_emotions_model(text)
                if response_data is None:
                    return Response({'error': f'{ERROR_MSG}'}, status=400)

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
                return Response({'error': f'{ERROR_MSG}'}, status=400)
        else:
            logger.error(
                f"An error occurred @api/emotion_analysis/{text_serializer.errors}")
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
                    return Response({"error": ERROR_MSG}, status=400)

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
            print(text_serializer.errors)
            logger.exception(
                f"An error occurred @api/gpt/completion/{text_serializer.errors}")
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


class InstructionCategoryCreateView(APIView):
    def post(self, request):
        # Get the 'name' field from the request data
        name = request.data.get('name')

        # Validate the 'name' field
        if not isinstance(name, str) or not name.strip():
            return Response({'error': 'Invalid name field.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid = validate_text_input(text=name)
        if is_valid[0] == False:
            return Response({'error': f'Invalid name field.{is_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the 'name' field already exists in the database
        if InstructionCategory.objects.filter(name__iexact=name).exists():
            return Response({'error': 'Instruction category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new InstructionCategory object with the given 'name' field
        obj = InstructionCategory.objects.create(
            name=name,
            created_by=request.user.id
        )

        # Serialize the new InstructionCategory object and return the serialized data in the response
        serializer = InstructionCategorySerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstructionCategoryListView(generics.ListAPIView):
    serializer_class = InstructionCategorySerializer

    def get_queryset(self):
        queryset = InstructionCategory.objects.all()
        search_query = self.request.query_params.get('q')
        # If the search query is present, filter the queryset by the name field
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class InstructionCategoryView(generics.RetrieveAPIView):
    serializer_class = InstructionCategorySerializer

    def get_queryset(self):
        return InstructionCategory.objects.filter(created_by=self.request.user.id)
    
class InstructionCategoryUpdateView(generics.UpdateAPIView):
    serializer_class = InstructionCategorySerializer

    def get_queryset(self):
        return InstructionCategory.objects.filter(created_by=self.request.user.id)


class CreateToneAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Tone detail required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the 'name' field
        is_valid, error_msg = validate_text_input(name)
        if not is_valid:
            return Response({'error': f'Invalid tone. {error_msg}'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the 'name' field already exists in the database
        if Tone.objects.filter(name__iexact=name).exists():
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


class ToneListView(generics.ListAPIView):
    serializer_class = ToneSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Tone.objects.all()
        # Instruction.objects.filter(user_id=self.request.user.id)
        # Get the search query parameter from the request
        search_query = self.request.query_params.get('q')

        # If the search query is present, filter the queryset by the name field
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class ToneRetrieveView(generics.RetrieveAPIView):
    serializer_class = ToneSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Tone.objects.all()

class ToneUpdateView(generics.RetrieveAPIView):
    serializer_class = ToneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tone.objects.filter(created_by=self.request.user.id)

class InstructionCreateView(APIView):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get data from request
        description = request.data.get('description')
        tones_data = self.request.data.get('tones')
        category_data = self.request.data.get('category')
        is_desc_valid = validate_text_input(text=description)

        # Validate data
        if is_desc_valid[0] == False:
            return Response({'error': f'Description is required. {is_desc_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)
        if not category_data:
            return Response({'error': 'Category is required.'}, status=status.HTTP_400_BAD_REQUEST)

        is_cat_valid = validate_text_input(text=category_data)

        if is_cat_valid[0] == False:
            return Response({'error': f'Category {is_cat_valid [1]}'}, status=status.HTTP_400_BAD_REQUEST)

        if not tones_data:
            return Response({'error': 'At least one tone is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if instruction with the same description already exists
        existing_inst = Instruction.objects.filter(description=description).first()
        if existing_inst:
            # If exists, return the existing instance
            serializer = InstructionSerializer(existing_inst)
            return Response(serializer.data, status=status.HTTP_200_OK)

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

        category, created = InstructionCategory.objects.get_or_create(name=category_data)
        if created:
            category.created_by = self.request.user.id
            category.save()

        inst_obj = Instruction.objects.create(
            description=description,
            category=category,
            created_by=request.user.id
        )
        inst_obj.tones.set(tones)
        inst_obj.save()
        serializer = InstructionSerializer(inst_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InstructionRetrieveView(generics.RetrieveAPIView):
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Instruction.objects.filter(created_by=self.request.user.id)


class InstructionUpdateView(APIView):
    serializer_class = InstructionSerializer
    permission_classes = [IsAuthenticated]

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
        category_name = request.data.get('category')

        if desc:
            instruction.description = desc

        if category_name:
            is_cat_valid = validate_text_input(text=category_name)
            if is_cat_valid[0]==False:
                return Response({'error': f'Invalid category. {is_cat_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)
            
            category, _ = InstructionCategory.objects.get_or_create(
                name=category_name)
            if category is None:
                return Response({'error': 'Invalid category'}, status=status.HTTP_400_BAD_REQUEST)
            instruction.category = category

        if tones:
            tones_data = []
            for tone_item in tones:
                is_tone_valid = validate_text_input(text=category_name)
                if is_tone_valid[0]==False:
                    return Response({'error': f'Invalid tone. {is_tone_valid[1]}'}, status=status.HTTP_400_BAD_REQUEST)
                tone, _ = Tone.objects.get_or_create(name=tone_item)
                if tone is None:
                    return Response({'error': f'Invalid tone: {tone_item}'}, status=status.HTTP_400_BAD_REQUEST)
                tones_data.append(tone)
            instruction.tones.set(tones_data)

        serializer = InstructionSerializerResult(instruction)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InstructionListView(generics.ListAPIView):
    serializer_class = InstructionSerializerResult
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Instruction.objects.all()

class InstructionSearchView(generics.ListAPIView):
    serializer_class = InstructionSerializerResult
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Instruction.objects.filter(created_by=self.request.user.id)
        description = self.request.query_params.get('description', None)
        category = self.request.query_params.get('category', None)
        tones = self.request.query_params.getlist('tones', [])

        if description is not None:
            queryset = queryset.filter(description__icontains=description)
        if category is not None:
            queryset = queryset.filter(category__name__icontains=category)
        if tones:
            queryset = queryset.filter(tones__name__in=tones).distinct()
        return queryset


