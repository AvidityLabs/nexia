# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from api.models import User


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
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, blank=True, null=True)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'Transaction #{self.id}: {self.amount} ({self.payment_type})'
