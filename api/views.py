import datetime
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import ValidationError

# Validate prompt text length
MAX_PROMPT_LENGTH = 1000  # Maximum allowed length for prompt text

from api.models import Prompt, User, UseCase, Tone, AIModel,   TokenUsage, PromptCategory
from api.serializers import (
    DeveloperRegisterSerializer,
    EmailAuthTokenSerializer,
    PromptSerializer,
    UseCaseSerializer,
    ToneSerializer,
    AIModelSerializer,
    CompletionSerializer,
    PromptCategorySerializer,
    CreateEditSerializer)

from api.utilities.openai import *
from api.middlewares.authentication import RapidAPIAuthentication


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


class UseCaseListCreateView(ListCreateAPIView):
    """
    For example, if you want to search for all UseCase objects with the name "authentication",
    you can make a GET request to /use-cases/?search=authentication.
    """
    queryset = UseCase.objects.all()
    serializer_class = UseCaseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        cat_name = request.data.get('category')
        cat, _  = PromptCategory.objects.get_or_create(name=cat_name)
        description = request.data.get('instruction')
        usecase, _ = UseCase.objects.get_or_create(
            category=cat,
            description=description,
        )
        return Response({'status': 'Use case created successfully'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

        


class UseCaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UseCase.objects.all()
    serializer_class = UseCaseSerializer


class ToneListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        search_query = request.query_params.get('search', None)
        if search_query:
            tones = Tone.objects.filter(name__icontains=search_query)
        else:
            tones = Tone.objects.all()
        serializer = ToneSerializer(tones, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ToneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tone.objects.all()
    serializer_class = ToneSerializer


class PromptCategoryListCreateView(generics.ListCreateAPIView):
    queryset = PromptCategory.objects.all()
    serializer_class = PromptCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PromptCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromptCategory.objects.all()
    serializer_class = PromptCategorySerializer


class PromptCreateView(generics.CreateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


"""
To use this view, you can send a GET request to the API with any of the following query parameters:

tone: The name of a tone to search for.
category: The name of a category to search for.
usecase: The name of a use case to search for.
For example, to search for prompts with the tone "happy", you would send a request to /prompts/?tone=happy.
If you want to search by multiple criteria, you can include multiple query parameters in the request, like this: /prompts/?tone=happy&category=food&usecase=conversation.
"""


class PromptSearchView(generics.ListAPIView):
    serializer_class = PromptSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tone__name', 'usecase__category__name', 'usecase__description']

    def get_queryset(self):
        queryset = Prompt.objects.all()
        tone = self.request.query_params.get('tone')
        category = self.request.query_params.get('category')
        usecase = self.request.query_params.get('usecase')

        if tone:
            queryset = queryset.filter(tone__name=tone)
        if category:
            queryset = queryset.filter(category__name=category)
        if usecase:
            queryset = queryset.filter(usecase__name=usecase)

        return queryset


class PromptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class AIModelsAPIView(APIView):
    serializer_class = AIModelSerializer

    def get(self, request):
        response = get_models()
        if response:
            for r in response.get('data'):
                obj, _ = AIModel.objects.get_or_create(id=r.get('id'))

            ai_models = AIModel.objects.all()
            serializer = AIModelSerializer(ai_models, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CreateEditAPIView(APIView):
    serializer_class = CreateEditSerializer

    def post(self, request):
        input_text = request.data.get('input', '')
        instruction_text = request.data.get('use_case', '')
        model = request.data.get('model', '')

        try:

            if len(input_text) > MAX_PROMPT_LENGTH:
                    raise ValidationError('Prompt text is too long.')
            user = User.objects.select_related(
                'subscription__pricing_plan').get(id=request.user.id)

            if not all([input_text, instruction_text, model]):
                return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user has reached token limit
            token_usage = TokenUsage.objects.filter(
                user=user,
                pricing_plan=user.subscription.pricing_plan,
                created_at__month=datetime.datetime.now().month,
                created_at__year=datetime.datetime.now().year
            ).first()

            if token_usage is not None and token_usage.total_tokens_used >= user.subscription.pricing_plan.token_limit:
                return Response({'error': 'Token limit reached. Please upgrade your plan.'}, status=status.HTTP_403_FORBIDDEN)

            response_data = create_edit(model, input_text, instruction_text)

            if response_data.get('usage') is None:
                return Response({'data': response_data}, status=status.HTTP_200_OK)

            obj_model, _ = AIModel.objects.get_or_create(id=model)
            token_usage, created = TokenUsage.objects.update_or_create(
                user=user,
                pricing_plan=user.subscription.pricing_plan,
                model=obj_model,
                defaults={
                    'prompt_tokens_used': response_data['usage'].get('prompt_tokens', 0),
                    'completion_tokens_used': response_data['usage'].get('completion_tokens', 0),
                    'total_tokens_used': response_data['usage'].get('total_tokens', 0)
                }
            )

            if not created:
                token_usage.prompt_tokens_used += response_data['usage'].get(
                    'prompt_tokens', 0)
                token_usage.completion_tokens_used += response_data['usage'].get(
                    'completion_tokens', 0)
                token_usage.total_tokens_used += response_data['usage'].get(
                    'total_tokens', 0)
                token_usage.save()

            return Response({'data': response_data}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=status.HTTP_404_NOT_FOUND)


class CompletionAPIView(APIView):
    serializer_class = CompletionSerializer

    def create_model(self, request, model_id):
        user = User.objects.get(id=request.user.id)
        obj_model, _ = AIModel.objects.get_or_create(id=model_id)

        # Check if user has exceeded their token limit
        pricing_plan = user.subscription.pricing_plan
        token_usage = TokenUsage.objects.filter(
            user=user,
            pricing_plan=pricing_plan,
            model=obj_model,
        ).first()
        if token_usage and token_usage.total_tokens_used >= pricing_plan.token_limit:
            raise ValidationError('Token limit exceeded.')

        return obj_model

    def post(self, request):
        serializer = CompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            obj_model = self.create_model(request, data['model'])
            prompt_text = data['prompt']
            use_saved_prompt = data['useSavedPrompt']
            prompt_id = data.get('promptId')
            max_tokens = data.get('max_tokens')
            temperature = data.get('temperature')
            top_p = data.get('top_p')
            n = data.get('n')
            stream = data.get('stream')
            logprobs = data.get('logprobs')
            stop = request.data.get('stop', '')

            prompt_info = None
            if use_saved_prompt:
                prompt_obj = Prompt.objects.get(id=prompt_id)
                prompt_info = prompt_obj.prompt
            else:
                prompt_info = prompt_text

            if len(prompt_info) > MAX_PROMPT_LENGTH:
                    raise ValidationError('Prompt text is too long.')

            # Generate completion
            response_data = create_completion(
                data['model'],
                prompt_info,
                max_tokens,
                temperature,
                top_p,
                n,
                stream,
                logprobs,
                stop,
            )

            # Track token usage
            user = User.objects.get(id=request.user.id)
            pricing_plan = user.subscription.pricing_plan
            prompt_tokens_used = response_data['usage'].get('prompt_tokens', 0)
            completion_tokens_used = response_data['usage'].get(
                'completion_tokens', 0)
            total_tokens_used = response_data['usage'].get('total_tokens', 0)
            token_usage, created = TokenUsage.objects.get_or_create(
                user=user,
                pricing_plan=pricing_plan,
                model=obj_model,
                defaults={
                    'prompt_tokens_used': prompt_tokens_used,
                    'completion_tokens_used': completion_tokens_used,
                    'total_tokens_used': total_tokens_used,
                }
            )

            if not created:
                token_usage.prompt_tokens_used += prompt_tokens_used
                token_usage.completion_tokens_used += completion_tokens_used
                token_usage.total_tokens_used += total_tokens_used
                token_usage.save()

            return Response({'data': response_data}, status=status.HTTP_200_OK)

        except TokenUsage.DoesNotExist:
            return Response({'error': 'Token usage not found.'}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400)
