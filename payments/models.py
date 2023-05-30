# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token




class Transaction(models.Model):
    PAYMENT_TYPES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('mpesa', 'Mpesa'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Add any additional fields you need for your transaction model

    def __str__(self):
        return f'Transaction #{self.id}: {self.amount} ({self.payment_type})'
