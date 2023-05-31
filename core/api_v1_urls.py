# Example 17.10: Combining Multiple App API Views Into One
# core/api_urls.py
"""Called from the project root's urls.py URLConf thus:
path('api/', include('core.api_urls', namespace='api')),
"""
from django.urls import path
from api  import views as api_views
from social_auth  import views as social_auth_views
from payments import views as payments_views

urlpatterns = [
path('social_auth', social_auth_views.SocialAuthView.as_view()),
path('get_token/', api_views.GetTokenAPIView.as_view(), name='get_token'),
path('register/',  api_views.UserRegisterView.as_view(), name="register"),
path('emotion/analysis/',  api_views.TextEmotionAnalysisView.as_view(), name='text-emotion-analysis'),
path('sentiment/analysis/',  api_views.TextSentimentAnalysisView.as_view(), name='text-sentiment-analysis'),
path('prompt/completion/',  api_views.ChatGPTCompletionView.as_view(), name='chatgpt-completion'),
path('prompt/create_edit/',  api_views.ChatGPTEditView.as_view(), name='chatgpt-completion'),
# path('text-to-image/', TextToImageView.as_view(), name='text-to-image'),
# path('text-to-video/', TextToVideoView.as_view(), name='text-to-video'),
#Tones
path('instructions/tones/create/',  api_views.CreateToneAPIView.as_view(), name='create-tone'),
path('instructions/tones/',  api_views.ToneListView.as_view(), name='tone-list'),
path('instructions/tones/detail/<int:pk>/',  api_views.ToneRetrieveView.as_view(), name='instruction-retrieve-update-destroy'),
path('instructions/tones/update/<int:pk>/',  api_views.ToneUpdateView.as_view(), name='instruction-retrieve-update-destroy'),
# Instructions
path('instructions/',  api_views.InstructionListView.as_view(), name='instruction-create'),
path('instructions/create/',  api_views.InstructionCreateView.as_view(), name='instruction-create'),
path('instructions/update/<int:pk>/',  api_views.InstructionUpdateView.as_view(), name='instruction-update'),
path('instructions/detail/<int:pk>/',  api_views.InstructionRetrieveView.as_view(), name='instruction-detail'),
path('instructions/search/',  api_views.InstructionSearchView.as_view(), name='instruction-search'),
path('drafts/',  api_views.DraftListCreateView.as_view(), name='draft-list-create'),
path('drafts/<int:pk>/',  api_views.DraftRetrieveUpdateDestroyView.as_view(), name='draft-retrieve-update-destroy'),
path('usecases/',  api_views.UseCasesList.as_view(), name='usecase_list'),
# Payments
path('home', payments_views.index, name='django_daraja_index'),
path('oauth/success', payments_views.oauth_success, name='test_oauth_success'),
path('stk-push/success', payments_views.STKPushAPIView.as_view(), name='test_stk_push_success'),
path('business-payment/success', payments_views.business_payment_success, name='test_business_payment_success'),
path('salary-payment/success', payments_views.salary_payment_success, name='test_salary_payment_success'),
path('promotion-payment/success', payments_views.promotion_payment_success, name='test_promotion_payment_success'),
# {% url 'api:flavors' flavor.uuid %}
# path(
# route='flavors/<uuid:uuid>/',
# view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
# name='flavors'
# ),
# # {% url 'api:users' %}
# path(
# route='users/',
# view=user_views.UserCreateReadView.as_view(),
# name='users'
# ),
# # {% url 'api:users' user.uuid %}
# path(
# route='users/<uuid:uuid>/',
# view=user_views.UserReadUpdateDeleteView.as_view(),
# name='users'
# ),
]
