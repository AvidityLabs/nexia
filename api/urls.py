
from django.urls import include, path
from api.views import (
    UserRetrieveUpdateAPIView,
    LoginAPIView,
    DeveloperRegisterView,
    TextEmotionAnalysisView,
    TextSentimentAnalysisView
    )


app_name = 'api'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('get_token/', LoginAPIView.as_view(), name='get_token'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('emotion/analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('sentiment/analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
]