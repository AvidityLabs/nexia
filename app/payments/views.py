# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from payments.mpesa import utils
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from payments.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime

cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'

def index(request):

	return HttpResponse('Welcome to the home of daraja APIs')

def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)


class STKPushAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = '0722212132'
        amount = 1
        account_reference = 'ABC001'
        transaction_desc = 'STK Push Description'
        callback_url = stk_push_callback_url
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        return Response(response.text, status=200)


def business_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Business Payment Description'
	occassion = 'Test business payment occassion'
	callback_url = b2c_callback_url
	r = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def salary_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Salary Payment Description'
	occassion = 'Test salary payment occassion'
	callback_url = b2c_callback_url
	r = cl.salary_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def promotion_payment_success(request):
	phone_number = config('B2C_PHONE_NUMBER')
	amount = 1
	transaction_desc = 'Promotion Payment Description'
	occassion = 'Test promotion payment occassion'
	callback_url = b2c_callback_url
	r = cl.promotion_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)


class  PayPalPayment(APIView):
	def post(request):
		# paypal_dict = {
		# 	'business': 'id@business.com',
		# 	'amount': 3,
		# 	'currency_code': 'GBP',
		# 	'item_name': 'book',
		# 	'notify_url':
		# }
		return Response(request.data, 200)