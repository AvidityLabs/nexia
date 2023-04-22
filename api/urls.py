
from django.urls import include, path
from api.views import (
    DeveloperRegisterView,
    ObtainEmailAuthToken,
    TextEmotionAnalysisView,
    TextSentimentAnalysisView
    )

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('get_token/',  ObtainEmailAuthToken.as_view(), name='api_token_auth'),
    path('register/', DeveloperRegisterView.as_view(), name="register"),
    path('emotion_analysis/', TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
    path('sentiment analysis/', TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
    


]