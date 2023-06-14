import os
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from api.serializers import InstructionSerializerResult
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock

import jwt
from api.models import *
from colorama import Fore, Style

import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)


JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
# TODO:add to environments
HTTP_X_RAPIDAPI_PROXY_SECRET = 'c7b970d0-dc8a-11ed-ba4c-f5094ac89edd'
HTTP_X_RAPIDAPI_HOST = 'nexia2.p.rapidapi.com'
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


"""
{'result': {'role': 'assistant', 'content': 'As an AI language model, I can generate text on a variety of topics, from current events and news to creative writing and poetry. I use deep learning and natural language processing algorithms to understand and generate human-like text that is coherent, relevant, and engaging. Whether you need a short article, a product description, or a social media post, I am capable of creating text that meets your specific needs and requirements. With my advanced language processing capabilities, I can analyze text to identify patterns and trends and generate content that is informative, entertaining, and appealing to readers. Whether you are a business owner, a marketer, or a content creator, I can help you take your message to the next level with high-quality text that resonates with your target audience.'}, 'prompt_tokens': 9, 'completion_tokens': 151, 'total_tokens_used': 160}
"""
def colorize(color, message):
    return f"{color}{message}{Style.RESET_ALL}"


def create_jwt_token(userId):
    from datetime import datetime
    from datetime import timedelta
    
    dt = datetime.now() + timedelta(days=60)
    exp_timestamp = int(dt.timestamp())

    token = jwt.encode({
        'id': str(userId),
        'exp': exp_timestamp
    }, JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_token(encoded_jwt):
    decoded_jwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
    return decoded_jwt


class DeveloperRegisterViewTest(TestCase):
    def setUp(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.GREEN, "Starting DeveloperRegisterViewTest..."))
        self.client = APIClient()
        # No Authorization header needed
        self.headers = {
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)

    def test_register_valid_credentials(self):
        response = self.client.post(
            reverse('api:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': 'testpass'}
        )

        subscription = Subscription.objects.all()[0]
        # Token Usage object created 
        token_usage_obj = TokenUsage.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(PricingPlan.objects.all()), 1)
        self.assertEqual(len(Subscription.objects.all()), 1)
        self.assertTrue('user' in response.json())
        self.assertEqual(type(subscription.pricing_plan.id), int)
        print(colorize(Fore.YELLOW, f"[Test Register] subscription created  plan NOTSET...{subscription.pricing_plan.name}"))
        self.assertEqual(subscription.pricing_plan.name, 'NOTSET')
        self.assertEqual(PricingPlan.objects.all()[0].name, 'NOTSET')
        self.assertEqual(len(token_usage_obj), 1)

    def test_register_invalid_credentials(self):
        response = self.client.post(
            reverse('api:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': ''}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(PricingPlan.objects.all()), 0)
        self.assertEqual(len(Subscription.objects.all()), 0)

    def tearDown(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.BLUE, "DeveloperRegisterViewTest Finished test."))

class ObtainEmailAuthTokenTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.YELLOW, f"Creating user with email 'test@test.com'..."))
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)


    def test_get_token_valid_credentials(self):

        print(colorize(Fore.YELLOW, "Sending POST request to get token..."))
        response = self.client.post(
            reverse('api:get_token'),
            {'email': 'test@test.com', 'password': 'password'}
        )

        subscription = Subscription.objects.all()[0]
 
        decoded_user_id = decode_token(response.json()['token'])['id']
        token_usage_obj = TokenUsage.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        print(colorize(Fore.YELLOW, f"[Test Register] subscription created  plan set to BASIC...{subscription.pricing_plan.name}"))
        # Expect NOTSET pricing plan by default then BASIC created when this api was called
        self.assertEqual(len(PricingPlan.objects.all()), 2)
        # Only one subscription should be created
        self.assertEqual(len(Subscription.objects.all()), 1)
        self.assertTrue('token' in response.json())
        self.assertEqual(type(subscription.pricing_plan.id), int)
        self.assertEqual(subscription.pricing_plan.name, 'BASIC')
        # at thsi point the basic pricing plan was created first
        self.assertEqual(PricingPlan.objects.all()[0].name, 'BASIC')
        self.assertEqual(decoded_user_id, str(self.user.id))
        self.assertEqual(len(token_usage_obj), 1)
        # Token usage updated 
        self.assertEqual(token_usage_obj[0].pricing_plan.name, 'BASIC')
        
        # self.assertEqual(decode_token(response.json()['token']['id'], JWT_SECRET_KEY), self.user.id)
        print(colorize(Fore.GREEN, "Obtain token test finished..."))

    def test_get_token_invalid_credentials(self):
        response = self.client.post(
            reverse('api:get_token'),
            {'email': 'test@test.com', 'password': 'wrongpass'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TextEmotionAnalysisViewTest(TestCase):
    def setUp(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.YELLOW, "Starting test..."))
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)



    def test_emotion_analysis_valid_text(self):
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            {'text': 'This is a happy text.'}
        )
        # print(response.json())
        token_usage = TokenUsage.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('analysis' in response.data)
        self.assertTrue(EMOTION_RESPONSE_DATA, response.json())

        self.assertEqual(token_usage[0].total_tokens_used, response.json()['total_tokens_used'])
        self.assertEqual(token_usage[0].prompt_tokens_used, response.json()['prompt_tokens'])
        self.assertEqual(token_usage[0].completion_tokens_used, response.json()['completion_tokens'])
        # Check token usage accounted for 

    def test_emotion_analysis_invalid_text(self):
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            {'text': ''}
        )
        token_usage = TokenUsage.objects.all()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_empty_text(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)


    def test_text_only_spaces(self):
        data = {
            'text': '     '
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_text_only_special_characters(self):
        data = {
            'text': '!@#$%^&*()'
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_text_only_digits(self):
        data = {
            'text': '1234567890'
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_non_ascii_characters(self):
        data = {
            'text': 'こんにちは'
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_text_too_long(self):
        data = {
            'text': 'a' * 2049
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def test_text_too_short(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            reverse('api:text-emotion-analysis'),
            data)
        self.assertEqual(response.status_code, 400)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(token_usage[0].total_tokens_used, 0)
        self.assertEqual(token_usage[0].prompt_tokens_used,0)
        self.assertEqual(token_usage[0].completion_tokens_used, 0)

    def tearDown(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.GREEN, "Finished test."))
class TextSentimentAnalysisViewTest(TestCase):
    def setUp(self):
        print(colorize(Fore.YELLOW, "Starting test..."))
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)

    def test_sentiment_analysis_valid_text(self):
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            {'text': 'This is a positive text.'}
        ) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('analysis' in response.data)
        token_usage = TokenUsage.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('analysis' in response.data)
        self.assertTrue(EMOTION_RESPONSE_DATA, response.json())

        self.assertEqual(token_usage[0].total_tokens_used, response.json()['total_tokens_used'])
        self.assertEqual(token_usage[0].prompt_tokens_used, response.json()['prompt_tokens'])
        self.assertEqual(token_usage[0].completion_tokens_used, response.json()['completion_tokens'])
        

    def test_sentiment_analysis_invalid_text(self):
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            {'text': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)

    def test_empty_text(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)


    def test_text_only_spaces(self):
        data = {
            'text': '     '
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_only_special_characters(self):
        data = {
            'text': '!@#$%^&*()'
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_only_digits(self):
        data = {
            'text': '1234567890'
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def test_non_ascii_characters(self):
        data = {
            'text': 'こんにちは'
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_too_long(self):
        data = {
            'text': 'a' * 2049
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_too_short(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            reverse('api:text-sentiment-analysis'),
            data)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        # Call the colorize function with the desired color and message to print to the console
        print(colorize(Fore.GREEN, "Finished test."))


class ChatGPTCompletionViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('api:chatgpt-completion')
        print(colorize(Fore.YELLOW, "Starting test..."))
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)


    def test_invalid_data(self):
        data = {'invalid_field': 'invalid_value'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': {'text': ['This field is required.']}})

    def test_invalid_text(self):
        data = {'text': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),  {'error': {'text': ['This field cannot be blank.']}})

    def test_empty_text(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)


    def test_text_only_spaces(self):
        data = {
            'text': '     '
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_only_special_characters(self):
        data = {
            'text': '!@#$%^&*()'
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_only_digits(self):
        data = {
            'text': '1234567890'
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)

    def test_non_ascii_characters(self):
        data = {
            'text': 'こんにちは'
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_too_long(self):
        data = {
            'text': 'a' * 2049
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)

    def test_text_too_short(self):
        data = {
            'text': ''
        }
        response = self.client.post(
            self.url,
            data)
        self.assertEqual(response.status_code, 400)


    def test_completion_error(self):
        data = {'text': 'some text'}
        with patch('api.views.completion', side_effect=Exception('Error')):
            response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Oops, something went wrong. If this issue persists, please contact our customer support team at aviditylabs@hotmail.com for assistance. We apologize for the inconvenience and appreciate your patience as we work to resolve the issue.'})

    def test_valid_data(self):
        data = {'text': 'hello'}
    
        # response = self.client.post(self.url, data=data)
        # print(response.json())
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue('result' in response.json())
        # token_usage = TokenUsage.objects.all()
        # self.assertEqual(token_usage[0].total_tokens_used, response.json()['total_tokens_used'])
        # self.assertEqual(token_usage[0].prompt_tokens_used, response.json()['prompt_tokens'])
        # self.assertEqual(token_usage[0].completion_tokens_used, response.json()['completion_tokens'])


  

class TestInstructionCategoryCreateView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)
        self.url = reverse('api:instruction-category-create')

    def test_valid_post_request(self):
        data = {'name': 'Test Category'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_invalid_post_request(self):
        data = {'name': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid name field.')

    def test_duplicate_post_request(self):
        InstructionCategory.objects.create(name='Test Category')
        data = {'name': 'Test Category'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Instruction category with this name already exists.')

    def test_invalid_name_field(self):
        data = {'name': 123}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid name field.Text cannot contain only digits')

    def test_name_field_with_special_characters(self):
        data = {'name': '#$%^&*'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid name field.Text cannot contain only special characters')


# Test case for InstructionCategoryListView

class TestInstructionCategoryListView(APITestCase):

    def setUp(self):
        print(colorize(Fore.YELLOW, "Starting test..."))
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)
        InstructionCategory.objects.create(name='Test Category 1')
        InstructionCategory.objects.create(name='Test Category 2')
        InstructionCategory.objects.create(name='Category Test 3')
        self.url = reverse('api:instruction-category-list')

    def test_get_all_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_search_categories(self):
        response = self.client.get(self.url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_search_categories_no_match(self):
        response = self.client.get(self.url, {'q': 'No match'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestCreateToneAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('api:create-tone')
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)

    def test_create_tone_success(self):
        data = {'name': 'Calm'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Calm')
        self.assertEqual(Tone.objects.count(), 1)

    def test_create_tone_missing_field(self):
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Tone detail required.')
        self.assertEqual(Tone.objects.count(), 0)

    def test_create_tone_invalid_field(self):
        data = {'name': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Tone detail required.')
        self.assertEqual(Tone.objects.count(), 0)

    def test_create_tone_already_exists(self):
        Tone.objects.create(name='Calm')
        data = {'name': 'Calm'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Tone with this name already exists.')
        self.assertEqual(Tone.objects.count(), 1)


class InstructionCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)

    def test_create_valid_instruction(self):
        url = reverse('api:instruction-create')
        data = {
            'description': 'Test instruction',
            'category': 'Test category',
            'tones': ['Test tone 1', 'Test tone 2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_instruction_with_invalid_description(self):
        url = reverse('instruction-create')
        data = {
            'description': '',
            'category': 'Test category',
            'tones': ['Test tone 1', 'Test tone 2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_instruction_with_invalid_category(self):
        url = reverse('instruction-create')
        data = {
            'description': 'Test instruction',
            'category': '',
            'tones': ['Test tone 1', 'Test tone 2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_instruction_with_invalid_tones(self):
        url = reverse('instruction-create')
        data = {
            'description': 'Test instruction',
            'category': 'Test category',
            'tones': ['', 'Test tone 2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InstructionRetrieveViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        self.client.credentials(**self.headers)
        self.instruction = Instruction.objects.create(
            description='Test instruction',
            category=InstructionCategory.objects.create(name='Test category'),
            created_by=self.user
        )

    def test_retrieve_valid_instruction(self):
        url = reverse('api:instruction-detail', kwargs={'pk': self.instruction.pk})
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_instruction(self):
        url = reverse('api:instruction-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class InstructionUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
        )
        self.user.set_password('password')
        self.user.save()
        print(colorize(Fore.GREEN, "User created successfully!"))
        self.token = self.user.token

        self.client = APIClient()
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.user.token}',
            'HTTP_X_RAPIDAPI_HOST': HTTP_X_RAPIDAPI_HOST,
            'HTTP_X_RAPIDAPI_PROXY_SECRET': HTTP_X_RAPIDAPI_PROXY_SECRET,
            'HTTP_X_RAPIDAPI_SUBSCRIPTION': HTTP_X_RAPIDAPI_SUBSCRIPTION
        }
        # self.instruction = Instruction.objects.create(
        #     description='Test instruction',
        #     category=InstructionCategory.objects.create(name='Test category'),
        #     created_by=self.user
        # )
        # self.instruction.tones.add(Tone.objects.create(name='Test tone'))

    # def test_update_instruction_with_valid_data(self):
    #     url = reverse('api:instruction-update', kwargs={'pk': self.instruction.pk})
    #     data = {
    #         'description': 'Updated test instruction',
    #         'category': 'Updated test category',
    #         'tones': ['Updated test tone']
    #     }
    #     response = self.client.put(url, data, format='json')
    #     instruction = Instruction.objects.get(pk=self.instruction.pk)
    #     serializer =  InstructionSerializerResult(instruction)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, serializer.data)

    # def test_update_instruction_with_invalid_category(self):
    #     url = reverse('api:instruction-update', kwargs={'pk': self.instruction.pk})
    #     data = {
    #         'category': 'Invalid category'
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_instruction_with_invalid_tone(self):
    #     url = reverse('api:instruction-update', kwargs={'pk': self.instruction.pk})
    #     data = {
    #         'tones': ['Invalid tone']
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_instruction_created_by_another_user(self):
    #     another_user = User.objects.create_user(
    #         username='anotheruser',
    #         email='testuser@email.com'
    #     )
    #     another_user.set_password('testpass')
    #     another_user.save()
    #     self.client.force_authenticate(user=another_user)
    #     url = reverse('api:instruction-update', kwargs={'pk': self.instruction.pk})
    #     data = {
    #         'description': 'Updated test instruction',
    #         'category': 'Updated test category',
    #         'tones': ['Updated test tone']
    #     }
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
