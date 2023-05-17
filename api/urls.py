
from django.urls import include, path
from api.views import (
    ToneUpdateView,
    UserRetrieveUpdateAPIView,
    GetTokenAPIView,
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
    ToneRetrieveView,
    CreateToneAPIView,
    ChatGPTEditView,
    DraftListCreateView,
    DraftRetrieveUpdateDestroyView,
    UseCasesList
    )


app_name = 'api'

urlpatterns = [
    # path('users/detail/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    # path('app/users/register/', AppUserRegisterView.as_view(), name='app-users-register'),
    path('v1/get_token/', GetTokenAPIView.as_view(), name='get_token'),
    path('v1/register/', DeveloperRegisterView.as_view(), name="register"),
    path('v1/emotion/analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('v1/sentiment/analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
    path('v1/prompt/completion/', ChatGPTCompletionView.as_view(), name='chatgpt-completion'),
    path('v1/prompt/create_edit/', ChatGPTEditView.as_view(), name='chatgpt-completion'),
    # pathv1/('text-to-image/', TextToImageView.as_view(), name='text-to-image'),
    # pathv1/('text-to-video/', TextToVideoView.as_view(), name='text-to-video'),
    #Tonesv1/
    path('v1/instructions/tones/create/', CreateToneAPIView.as_view(), name='create-tone'),
    path('v1/instructions/tones/', ToneListView.as_view(), name='tone-list'),
    path('v1/instructions/tones/detail/<int:pk>/', ToneRetrieveView.as_view(), name='instruction-retrieve-update-destroy'),
    path('v1/instructions/tones/update/<int:pk>/', ToneUpdateView.as_view(), name='instruction-retrieve-update-destroy'),
    # Instv1/ructions
    path('v1/instructions/', InstructionListView.as_view(), name='instruction-create'),
    path('v1/instructions/create/', InstructionCreateView.as_view(), name='instruction-create'),
    path('v1/instructions/update/<int:pk>/', InstructionUpdateView.as_view(), name='instruction-update'),
    path('v1/instructions/detail/<int:pk>/', InstructionRetrieveView.as_view(), name='instruction-detail'),
    path('v1/instructions/search/', InstructionSearchView.as_view(), name='instruction-search'),
    path('drafts/', DraftListCreateView.as_view(), name='draft-list-create'),
    path('drafts/<int:pk>/', DraftRetrieveUpdateDestroyView.as_view(), name='draft-retrieve-update-destroy'),
    path('v1/usecases/', UseCasesList.as_view(), name='usecase_list'),


    

  
]