
from django.urls import include, path
from api.views import (
    DeveloperRegisterView,
    ObtainEmailAuthToken,
    TextEmotionAnalysisView,
    TextSentimentAnalysisView
    )


app_name = 'api'

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('get_token/',  ObtainEmailAuthToken.as_view(), name='get_token'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('emotion_analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('sentiment_analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
]