import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from api.models import (PricingPlan, User, Subscription)


HTTP_X_RAPIDAPI_PROXY_SECRET = os.environ.get('HTTP_X_RAPIDAPI_PROXY_SECRET')
HTTP_X_RAPIDAPI_HOST = os.environ.get('HTTP_X_RAPIDAPI_HOST')
TEST_HTTP_AUTHORIZATION = os.environ.get('TEST_HTTP_AUTHORIZATION')
HTTP_X_RAPIDAPI_SUBSCRIPTION = 'BASIC'
SENTIMENT_RESPONSE_DATA = [
    [
        {
            "label": "negative",
            "score": 0.001586591126397252,
            "percentage": 0.16
        },
        {
            "label": "neutral",
            "score": 0.00463769631460309,
            "percentage": 0.46
        },
        {
            "label": "positive",
            "score": 0.9937757253646851,
            "percentage": 99.38
        }
    ]
]

EMOTION_RESPONSE_DATA=[
    [
        {
            "label": "joy",
            "score": 0.9837275743484497,
            "percentage": 98.37
        },
        {
            "label": "surprise",
            "score": 0.0065237125381827354,
            "percentage": 0.65
        },
        {
            "label": "neutral",
            "score": 0.0061690774746239185,
            "percentage": 0.62
        },
        {
            "label": "disgust",
            "score": 0.0010919542983174324,
            "percentage": 0.11
        },
        {
            "label": "sadness",
            "score": 0.0010498764459043741,
            "percentage": 0.1
        },
        {
            "label": "anger",
            "score": 0.000743839715141803,
            "percentage": 0.07
        },
        {
            "label": "fear",
            "score": 0.0006939407321624458,
            "percentage": 0.07
        }
    ]
]

class ObtainEmailAuthTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass',
            api_key='testapikey'
        )
        Token.objects.create(user=self.user)

        # self.user = User.objects.create_user(
        #     email='test@test.com',
        #     password='testpass'
        # )

    # def test_get_token_valid_credentials(self):
    #     response = self.client.post(
    #         reverse('api:get_token'),
    #         {'email': 'test@test.com', 'password': 'testpass'}
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue('token' in response.data)

    # def test_get_token_invalid_credentials(self):
    #     response = self.client.post(
    #         reverse('api:get_token'),
    #         {'email': 'test@test.com', 'password': 'wrongpass'}
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeveloperRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=HTTP_X_RAPIDAPI_PROXY_SECRET)
        self.client.credentials(HTTP_X_RAPIDAPI_HOST=HTTP_X_RAPIDAPI_HOST)
        self.client.credentials(
            HTTP_X_RAPIDAPI_PROXY_SECRET=HTTP_X_RAPIDAPI_PROXY_SECRET)
        self.client.credentials(
            HTTP_X_RAPIDAPI_SUBSCRIPTION=HTTP_X_RAPIDAPI_SUBSCRIPTION)

    def test_register_valid_credentials(self):
        response = self.client.post(
            reverse('api:register'),
            {'email': 'test@test.com', 'password': 'testpass'}
        )
        subscription = Subscription.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(PricingPlan.objects.all()), 1)
        self.assertEqual(len(Subscription.objects.all()), 1)
        self.assertTrue('api_key' in response.data)
        self.assertEqual(type(subscription.pricing_plan.id), int)

    def test_register_invalid_credentials(self):
        response = self.client.post(
            reverse('api:register'),
            {'email': 'test@test.com', 'password': ''}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)
        self.assertEqual(len(PricingPlan.objects.all()), 0)
        self.assertEqual(len(Subscription.objects.all()), 0)


class TextEmotionAnalysisViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass'
        )
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_emotion_analysis_valid_text(self):
        response = self.client.post(
            reverse('text-emotion-analysis'),
            {'text': 'This is a happy text.'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('emotions' in response.data)

    def test_emotion_analysis_invalid_text(self):
        response = self.client.post(
            reverse('text-emotion-analysis'),
            {'text': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('text' in response.data)

# class TextSentimentAnalysisViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@test.com',
#             password='testpass'
#         )
#         token, _ = Token.objects.get_or_create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

#     def test_sentiment_analysis_valid_text(self):
#         response = self.client.post(
#             reverse('text-sentiment-analysis'),
#             {'text': 'This is a positive text.'}
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('score' in response.data)

#     def test_sentiment_analysis_invalid_text(self):
#         response = self.client.post(
#             reverse('text-sentiment-analysis'),
#             {'text': ''}
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertTrue('text' in response.data)
