
from django.urls import include, path
from api.views import (
    # CategorySearchView,
    InstructionCategoryUpdateView,
    ToneUpdateView,
    UserRetrieveUpdateAPIView,
    LoginAPIView,
    DeveloperRegisterView,
    TextEmotionAnalysisView,
    TextSentimentAnalysisView,
    ChatGPTCompletionView,
    TextToImageView,
    TextToVideoView,
    AppUserRegisterView,
    InstructionRetrieveView,
    InstructionListView,
    InstructionCreateView,
    InstructionUpdateView,
    InstructionSearchView,
    ToneListView,
    InstructionCategoryCreateView,
    InstructionCategoryListView,
    ToneRetrieveView,
    CreateToneAPIView
    )


app_name = 'api'

urlpatterns = [
    # path('users/', UserRetrieveUpdateAPIView.as_view(), name='users'),
    # path('app/users/register/', AppUserRegisterView.as_view(), name='app-users-register'),
    path('get_token/', LoginAPIView.as_view(), name='get_token'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('emotion/analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('sentiment/analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
    path('prompt/completion/', ChatGPTCompletionView.as_view(), name='chatgpt-completion'),
    # path('text-to-image/', TextToImageView.as_view(), name='text-to-image'),
    # path('text-to-video/', TextToVideoView.as_view(), name='text-to-video'),
    #Tones
    path('instructions/tones/create/', CreateToneAPIView.as_view(), name='create-tone'),
    path('instructions/tones/', ToneListView.as_view(), name='tone-list'),
    path('instructions/tones/detail/<int:pk>/', ToneRetrieveView.as_view(), name='instruction-retrieve-update-destroy'),
    path('instructions/tones/update/<int:pk>/', ToneUpdateView.as_view(), name='instruction-retrieve-update-destroy'),
    # Instruction Categories
    path('instructions/categories/create/', InstructionCategoryCreateView.as_view(), name='instruction-category-create'),
    path('instructions/categories/detail/<int:pk>/', InstructionCategoryCreateView.as_view(), name='instruction-category-create'),
    path('instructions/categories/update/<int:pk>/', InstructionCategoryUpdateView.as_view(), name='instruction-category-update'),
    path('instructions/categories/', InstructionCategoryListView.as_view(), name='instruction-category-list'),
    # Instructions
    path('instructions/', InstructionListView.as_view(), name='instruction-create'),
    path('instructions/create/', InstructionCreateView.as_view(), name='instruction-create'),
    path('instructions/update/<int:pk>/', InstructionUpdateView.as_view(), name='instruction-update'),
    path('instructions/detail/<int:pk>/', InstructionRetrieveView.as_view(), name='instruction-detail'),
    path('instructions/search/', InstructionSearchView.as_view(), name='instruction-search'),


    

  
]