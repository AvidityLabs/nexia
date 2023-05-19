from django.urls import path

from .views import SocialAuthView

social_auth = 'social_auth'
urlpatterns = [
    path('', SocialAuthView.as_view()),

]