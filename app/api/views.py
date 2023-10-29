import json
import logging
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from api.email import send_email_to_user
from api.utilities.validators.text_validator import validate_text_input
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from api.utilities.tokens import MonthlyTokenLimitExceeded
from api.utilities.tokens import validate_token_usage
from api.renderers import APIJSONRenderer
from .models import Instruction, PricingPlan, TextToImage, TextToVideo, TokenUsage, Tone, User
from documents.models import (Document)
from usecases.models import (
    UseCase
)
from .serializers import  AnyPayloadSerializer, DocumentSerializer, InstructionSerializer, InstructionSerializerResult, TextCompletionSerializer, TextToImageSerializer, TextToVideoSerializer, ToneSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
# from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from api.renderers import UserJSONRenderer
from api.utilities.hugging_face.queries import query_emotions_model, query_sentiment_model
from api.utilities.hugging_face.utils import rename_sentiment_labels, add_emotion_percentages
from api.utilities.tokens import update_token_usage
from api.utilities.openai.utils import completion, edit
from api.utilities.hugging_face.tokenizer import calculate_tokens
from api.utilities.jwt_helper import decode_jwt_token
from api.utilities.tones_list import TONES
# from api.prompts.repository import promptExecute
from api.serializers import (
    UserRegisterSerializer,
    TextSerializer,
    LoginSerializer,
    UserSerializer,
    TextToImageSerializer,
    TextToVideoSerializer
)
from usecases.serializers import UseCaseSerializer

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


class EmailComfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)
    def get(request):
        if request.user is None:
            return Response({'error': 'Invalid user credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        user= json.dumps(request.user)
        return Response(request.user)



class GetActiveUserAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)
    def get(self, request):
        if request.user is None:
            return Response({'error': 'Invalid user credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = LoginSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def post(self, request):
        user = request.user
        try:
            # Get the current and new passwords from the request data
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            print(user.check_password(current_password))
            print(request.data)
            # Verify if the current password is correct
            if not user.check_password(current_password):
                return Response({'error': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password with the new password
            user.set_password(new_password)
            user.save()

            # try:
            #     # Send email notification to the user
            #     send_mail(
            #         'Password Changed',
            #         'Your password has been successfully changed.',
            #         'from@example.com',
            #         [user.email],
            #         fail_silently=False,
            #     )
            # except Exception as e:
            #     # Handle any exception that occurs while sending the email
            #     return Response({'error': 'Failed to send email notification'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Serialize the user object and return the response
            serializer = LoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), 400)



class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def post(self, request):
        user = request.user
        try:
            # Get the current and new email from the request data
            current_email = request.data.get('current_email')
            new_email = request.data.get('new_email')

            if user.email == new_email:
                return Response({'error': 'Invalid current email and new email are the same'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify if the current email is correct
            if user.email != current_email:
                return Response({'error': 'Invalid current email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new email already exists in the system
            if User.objects.filter(email=new_email).exists():
                return Response({'error': 'New email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's email with the new email
            user.email = new_email
            user.save()

            # Uncomment the following code if you want to send an email notification to the user
            """
            try:
                # Send email notification to the user
                send_mail(
                    'Email Changed',
                    'Your email has been successfully changed.',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Handle any exception that occurs while sending the email
                return Response({'error': 'Failed to send email notification'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            """

            # Serialize the user object and return the response
            serializer = LoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def get(self, request):
        user = request.user
        try:
            # Perform the user deletion logic here
            user.delete()

            # Optionally, you can send a response with a success message
            # # Send email notification to the user
            # send_mail(
            #     'Email Changed',
            #     'Your email has been successfully changed.',
            #     'from@example.com',
            #     [user.email],
            #     fail_silently=False,
            # )
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exception that occurs during user deletion
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            name = request.data.get('name')
            
            if name:
                user.display_name = name
                user.save()
                
            serializer = UserSerializer(user)
            return Response({'msg': 'Updated..', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'msg': 'Unauthorized change profile', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "password": request.data.get('password')
        }
        print(user)
        try:
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "username": request.data.get('email'),
            "password": request.data.get('password'),
            "pricing_plan": request.data.get('pricing_plan')
        }
        serializer = self.serializer_class(data=user)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_email_to_user(user.get('email'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        # NOTE CODE TO VALIDATE TOKEN 
        # validate_token_usage(request.user)

        # text_serializer = AnyPayloadSerializer(data=request.data)
 
        try:
            from usecases.models import UseCase
            usecase= UseCase.objects.filter(navigateTo=request.data.get('payload')['usecase'])

            if not usecase.exists():
                return Response({'error': 'Use case not found'}, status=status.HTTP_400_BAD_REQUEST)
            response = usecase[0].promptExecute(request.data.get('payload'))
            # print(response)
            # response = promptExecute(request.data.get('payload')['usecase'], request.data.get('payload'))

            if response is None:
                return Response({'error': 'Unable to communicate with the GPT model'}, status=status.HTTP_400_BAD_REQUEST)

            prompt_tokens = response['token_usage']['prompt_tokens']
            completion_tokens = response['token_usage']['completion_tokens']
            total_tokens = response['token_usage']['total_tokens']

            # # # # Track token usage
            user = request.user
            

            result = {
                "result": {
                    "content": response['res']['kwargs']['content'],
                    "role": ''
                },
                "prompt_tokens": response['token_usage']['prompt_tokens'],
                "completion_tokens": response['token_usage']['completion_tokens'],
                "total_tokens_used": response['token_usage']['total_tokens']
            }
            # # Assuming user and num_tokens are defined update token usage use background tasks
            update_token_usage(user, prompt_tokens,
                                completion_tokens, total_tokens)
            return Response(result, status=200)
        except Exception as e:
            print(e)
            logger.error(f"An error occurred @api/gpt/completion/: {e}")
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


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

# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ToneListView(generics.ListAPIView):
    serializer_class = ToneSerializer
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)


    def get_queryset(self):
        queryset = Tone.objects.all()
        # Create tones if they dont exist
        #TDODO AUTOMATE THIS 
        # if len(queryset)==0:
        #     Tone.objects.bulk_create([Tone(name=t) for t in TONES])
                
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

class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = (APIJSONRenderer,)

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            use_case = request.data.get('use_case')
            title = request.data.get('title')
            content = request.data.get('content')

            use_case = UseCase.objects.get(navigateTo=use_case)

            # Check if a document with the same title exists
            existing_document = Document.objects.filter(title=title).first()
            
            if existing_document and existing_document.content == content:
                # Document with the same title and content already exists
                serializer = DocumentSerializer(existing_document)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            if existing_document:
                # Update the existing document with the new content
                existing_document.content = content
                existing_document.save()
                serializer = DocumentSerializer(existing_document)
                return Response(serializer.data, status=status.HTTP_200_OK)

            draft = Document(user=user, document_type="html", use_case=use_case, title=title, content=content)
            draft.save()

            serializer = DocumentSerializer(draft)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except UseCase.DoesNotExist as e:
            print(e)
            return Response({'error': 'Invalid use case'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class UseCasesList(APIView):
    queryset = UseCase.objects.all()

    def get(self, request):
       #Only limit to thses features at the moment 
        current_features = [
        "youtube_video_description",
        "grammar_correction"
        "social_media_post",
        "summarize_text",
        "generate_video_script"
        ]
    
        # Filter UseCase objects where navigateTo is in current_features
        filtered_usecases = self.queryset.filter(navigateTo__in=current_features)

        # Serialize the filtered UseCase objects
        serializer = UseCaseSerializer(filtered_usecases, many=True)

        return Response(serializer.data)