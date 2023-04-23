import os
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from api.models import (PricingPlan, User, Subscription, TokenUsage)
from colorama import Fore, Style

import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)



# TODO:add to environments
HTTP_X_RAPIDAPI_PROXY_SECRET = 'c7b970d0-dc8a-11ed-ba4c-f5094ac89edd'
HTTP_X_RAPIDAPI_HOST = 'test'
TEST_HTTP_AUTHORIZATION = 'test'
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

EMOTION_RESPONSE_DATA = {
    "analysis": [
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
}

def colorize(color, message):
    return f"{color}{message}{Style.RESET_ALL}"


class DeveloperRegisterViewTest(TestCase):
    def setUp(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.GREEN, "Starting test..."))
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
            {'username': 'eddy', 'email': 'test@test.com', 'password': 'testpass'}
        )
        # subscription = Subscription.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(len(PricingPlan.objects.all()), 1)
        # self.assertEqual(len(Subscription.objects.all()), 1)
        # self.assertTrue('api_key' in response.data)
        # self.assertEqual(type(subscription.pricing_plan.id), int)

    def test_register_invalid_credentials(self):
        response = self.client.post(
            reverse('api:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': ''}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(len(PricingPlan.objects.all()), 0)
        # self.assertEqual(len(Subscription.objects.all()), 0)

    def tearDown(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.GREEN, "Finished test."))

# class ObtainEmailAuthTokenTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()


#     def test_get_token_valid_credentials(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Starting test..."))
#         self.plan = PricingPlan.objects.create(name='BASIC')
#         self.subscription = Subscription.objects.create(
#             pricing_plan=self.plan
#         )
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@test.com',
#             password='password',
#             subscription=self.subscription
#         )
 
#         self.token = Token.objects.create(user=self.user)
#         self.user.api_key = self.token.key
#         self.user.save()
#         self.client = APIClient()
#         self.headers = {
#             'HTTP_AUTHORIZATION': f'{self.token.key}',
#             'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
#             'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
#             'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
#         }
#         self.client.credentials(**self.headers)


#         user = User.objects.filter(api_key=self.token)[0]
#         response = self.client.post(
#             reverse('api:get_token'),
#             {'email': 'test@test.com', 'password': 'password'}
#         )
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('token' in response.data)

    # def test_get_token_invalid_credentials(self):
    #     response = self.client.post(
    #         reverse('api:get_token'),
    #         {'email': 'test@test.com', 'password': 'wrongpass'}
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class TextEmotionAnalysisViewTest(TestCase):
#     def setUp(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Starting test..."))
#         self.plan = PricingPlan.objects.create(name='BASIC')
#         self.subscription = Subscription.objects.create(
#             pricing_plan=self.plan
#         )
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@test.com',
#             subscription=self.subscription
#         )
 
#         self.token = Token.objects.create(user=self.user)
#         self.user.api_key = self.token.key
#         self.user.save()
#         self.client = APIClient()
#         self.headers = {
#             'HTTP_AUTHORIZATION': f'{self.token.key}',
#             'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
#             'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
#             'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
#         }
#         self.client.credentials(**self.headers)

#     def test_emotion_analysis_valid_text(self):
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             {'text': 'This is a happy text.'}
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('analysis' in response.data)
#         self.assertTrue(EMOTION_RESPONSE_DATA, response.json())

#     def test_emotion_analysis_invalid_text(self):
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             {'text': ''}
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertTrue('error' in response.data)

#     def test_empty_text(self):
#         data = {
#             'text': ''
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)


#     def test_text_only_spaces(self):
#         data = {
#             'text': '     '
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_only_special_characters(self):
#         data = {
#             'text': '!@#$%^&*()'
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_only_digits(self):
#         data = {
#             'text': '1234567890'
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_non_ascii_characters(self):
#         data = {
#             'text': 'こんにちは'
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_too_long(self):
#         data = {
#             'text': 'a' * 2049
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_too_short(self):
#         data = {
#             'text': ''
#         }
#         response = self.client.post(
#             reverse('api:text-emotion-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def tearDown(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Finished test."))
# class TextSentimentAnalysisViewTest(TestCase):
#     def setUp(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Starting test..."))
#         self.plan = PricingPlan.objects.create(name='BASIC')
#         self.subscription = Subscription.objects.create(
#             pricing_plan=self.plan
#         )
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@test.com',
#             subscription=self.subscription
#         )
 
#         self.token = Token.objects.create(user=self.user)
#         self.user.api_key = self.token.key
#         self.user.save()
#         self.client = APIClient()
#         self.headers = {
#             'HTTP_AUTHORIZATION': f'{self.token.key}',
#             'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
#             'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
#             'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
#         }
#         self.client.credentials(**self.headers)

#     def test_sentiment_analysis_valid_text(self):
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             {'text': 'This is a positive text.'}
#         ) 

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('analysis' in response.data)
        

#     def test_sentiment_analysis_invalid_text(self):
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             {'text': ''}
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertTrue('error' in response.data)

#     def test_empty_text(self):
#         data = {
#             'text': ''
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)


#     def test_text_only_spaces(self):
#         data = {
#             'text': '     '
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_only_special_characters(self):
#         data = {
#             'text': '!@#$%^&*()'
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_only_digits(self):
#         data = {
#             'text': '1234567890'
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_non_ascii_characters(self):
#         data = {
#             'text': 'こんにちは'
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_too_long(self):
#         data = {
#             'text': 'a' * 2049
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def test_text_too_short(self):
#         data = {
#             'text': ''
#         }
#         response = self.client.post(
#             reverse('api:text-sentiment-analysis'),
#             data)
#         self.assertEqual(response.status_code, 400)

#     def tearDown(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Finished test."))


# class TextSentimentAnalysisViewTest(TestCase):
#     def setUp(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Starting test..."))
#         self.plan = PricingPlan.objects.create(name='BASIC')
#         self.subscription = Subscription.objects.create(
#             pricing_plan=self.plan
#         )
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@test.com',
#             subscription=self.subscription
#         )
 
#         self.token = Token.objects.create(user=self.user)
#         self.user.api_key = self.token.key
#         self.user.save()
#         self.client = APIClient()
#         self.headers = {
#             'HTTP_AUTHORIZATION': f'{self.token.key}',
#             'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
#             'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
#             'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
#         }
#         self.client.credentials(**self.headers)
#     def test_connection_error(self):
#         with mock.patch('api.utilities.hugging_face.query_sentiment_model') as mock_query:
#             mock_query.side_effect = ConnectionError('Connection refused')
#             url = reverse('api:text-sentiment-analysis')
#             data = {'text': 'This is a test'}

#             # response = self.client.post(url, data, format='json')
#             # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             # self.assertEqual(response.data, {
#             #     'error': 'Something went wrong. If this issue persists please contact us through our customer support at aviditylabs@hotmail.com'})


# class TextEmotionAnalysisViewTest(TestCase):
#     def setUp(self):
#         # Call the colorize function with the desired color and message to print to the console
#         print(colorize(Fore.GREEN, "Starting test..."))
#         self.plan = PricingPlan.objects.create(name='BASIC')
#         self.subscription = Subscription.objects.create(
#             pricing_plan=self.plan
#         )
#         self.user = User.objects.create(
#             username='testuser',
#             email='test@test.com',
#             subscription=self.subscription
#         )
 
#         self.token = Token.objects.create(user=self.user)
#         self.user.api_key = self.token.key
#         self.user.save()
#         self.client = APIClient()
#         self.headers = {
#             'HTTP_AUTHORIZATION': f'{self.token.key}',
#             'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
#             'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
#             'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
#         }
#         self.client.credentials(**self.headers)
#     def test_connection_error(self):
#         with mock.patch('api.utilities.hugging_face.query_emotions_model') as mock_query:
#             mock_query.side_effect = ConnectionError('Connection refused')
#             url = reverse('api:text-emotion-analysis')
#             data = {'text': 'This is a test'}

#             response = self.client.post(url, data, format='json')
#             # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             # self.assertEqual(response.data, {
#             #     'error': 'Something went wrong. If this issue persists please contact us through our customer support at aviditylabs@hotmail.com'})