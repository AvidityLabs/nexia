import uuid
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

# views.py
from rest_framework import generics
from .models import Prompt, UseCase, Tone, AIModel,   TokenUsage, PromptCategory
from .serializers import (
    DeveloperRegisterSerializer,
    PromptSerializer,
    UseCaseSerializer,
    ToneSerializer,
    AIModelSerializer,
    CompletionSerializer,
    PromptCategorySerializer,
     CreateEditSerializer)


from .models import User
from .utilities.openai import *

# view for registering developers


class DeveloperRegisterView(generics.CreateAPIView):
    serializer_class = DeveloperRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.create(
                    email=email,
                    first_name=email,
                    username=email,
                    is_developer=True)
                user.set_password(password)

                token = Token.objects.create(user=user)
                user.developer_id = token.key
                user.save()

                return Response({'api_key': token.key}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UseCaseListCreateView(APIView):
    def get(self, request, format=None):
        search_query = request.query_params.get('search', None)
        if search_query:
            use_cases = UseCase.objects.filter(name__icontains=search_query)
        else:
            use_cases = UseCase.objects.all()
        serializer = UseCaseSerializer(use_cases, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UseCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UseCaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UseCase.objects.all()
    serializer_class = UseCaseSerializer


class ToneListCreateView(generics.ListCreateAPIView):
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
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tone__name', 'category__name', 'usecase__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        tone = self.request.query_params.get('tone', None)
        category = self.request.query_params.get('category', None)
        usecase = self.request.query_params.get('usecase', None)
        
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
    serializer_class =  CreateEditSerializer
    def post(self, request):
        # Retrieve input, instruction, and parameters from request data
        input_text = request.data.get('input', '')
        instruction_text = request.data.get('use_case', '')
        model = request.data.get('model', '')

        # Validate above must not be null
        if not all([input_text, instruction_text, model]):
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=request.user.id)

            response_data = create_edit(model, input_text, instruction_text)
            if response_data.get('usage', None) is None:
                return Response(status=status.HTTP_200_OK, data=response_data)
            obj_model, _ = AIModel.objects.get_or_create(id=model)
            # Track token usage
            TokenUsage.objects.create(
                user=user,
                model=obj_model,
                prompt_tokens_used=response_data['usage'].get('prompt_tokens'),
                completion_tokens_used=response_data['usage'].get(
                    'completion_tokens'),
                total_tokens_used=response_data['usage'].get('total_tokens')
            )
            # Return the generated text in a JSON response
            return Response({'data': response_data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=status.HTTP_404_NOT_FOUND)


class CompletionAPIView(APIView):
    serializer_class =  CompletionSerializer
    def post(self, request):
        serializer = CompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(id=request.user.id)
            model_id = data['model']
            prompt_text = data['prompt']
            prompt_id = data['promptId']
            useSavedPrompt = data['useSavedPrompt']
            max_tokens = data.get('max_tokens')
            temperature = data.get('temperature')
            top_p = data.get('top_p')
            n = data.get('n')
            stream = data.get('stream')
            logprobs = data.get('logprobs')
            stop = request.data.get('stop')

            promptInfo = None
            if useSavedPrompt:
                prompt_obj = Prompt.objects.get(id=prompt_id)
                promptInfo = prompt_obj.prompt
                print(promptInfo)
            else:
                promptInfo = prompt_text

            # # Return the generated text in a JSON response
            res = create_completion(
                model_id,
                promptInfo,
                max_tokens,
                temperature,
                top_p,
                n,
                stream,
                logprobs,
                stop)

            if res.get('usage', None) is None:
                return Response(status=status.HTTP_404_NOT_FOUND, data=res)
            # Track token usage
            TokenUsage.objects.create(
                user=user,
                model=model_id,
                prompt_tokens_used=res['usage'].get('prompt_tokens'),
                completion_tokens_used=res['usage'].get('completion_tokens'),
                total_tokens_used=res['usage'].get('total_tokens')
            )
            return Response({'data': res}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
