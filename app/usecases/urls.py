from django.urls import path
from .views import GenerateEmailView

urlpatterns = [
    path('generate-email/', GenerateEmailView.as_view(), name='generate-email'),
]