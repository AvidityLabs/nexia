
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    DeveloperRegisterView,
    PromptCreateView,
    PromptSearchView,
    PromptDetailView,
    UseCaseListCreateView,
    ToneListCreateView,
    ToneDetailView,
    UseCaseDetailView,
    AIModelsAPIView,
    CreateEditAPIView,
    CompletionAPIView,
    PromptCategoryListCreateView,
    ObtainEmailAuthToken
    )

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('get_token/',  ObtainEmailAuthToken, name='api_token_auth'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('use_cases/', UseCaseListCreateView.as_view(), name='use-case-list-create'),
    path('use_cases/<int:pk>/', UseCaseDetailView.as_view(), name='use-case-detail'),
    path('tones/', ToneListCreateView.as_view(), name='tone-list-create'),
    path('tones/<int:pk>/', ToneDetailView.as_view(), name='tone-detail'),
    path('prompt_categories/', PromptCategoryListCreateView.as_view(), name='prompt-categories-list-create'),
    path('create_prompt/', PromptCreateView.as_view(), name='create-prompt'),
    path('prompts/', PromptSearchView.as_view(), name='prompts'),
    path('prompts/<int:pk>/', PromptDetailView.as_view(), name='prompt-detail'),
    path('models/', AIModelsAPIView.as_view(), name='models'),
    path('create_edit/', CreateEditAPIView.as_view(), name='create-edits'),
    path('create_completion/', CompletionAPIView.as_view(), name='create-completion'),


]