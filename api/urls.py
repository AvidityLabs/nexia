
from django.urls import include, path
from api.views import (
    UserRetrieveUpdateAPIView,
    LoginAPIView,
    DeveloperRegisterView,
    TextEmotionAnalysisView,
    TextSentimentAnalysisView,
    ChatGPTCompletionView,
    TextToImageView,
    TextToVideoView,
    AppUserRegisterView
    )


app_name = 'api'

urlpatterns = [
    # path('users/', UserRetrieveUpdateAPIView.as_view(), name='users'),
    # path('app/users/register/', AppUserRegisterView.as_view(), name='app-users-register'),
    path('get_token/', LoginAPIView.as_view(), name='get_token'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('emotion/analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('sentiment/analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
    path('prompt/completion/', ChatGPTCompletionView.as_view(), name='gpt/completion'),
    path('text-to-image/', TextToImageView.as_view(), name='text-to-image'),
    path('text-to-video/', TextToVideoView.as_view(), name='text-to-video'),
  
]