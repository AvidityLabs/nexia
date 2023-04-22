import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class PricingPlan(BaseModel):
    BASIC = 'basic'
    PRO = 'pro'
    ULTRA = 'ultra'
    MEGA = 'mega'
    CUSTOM = 'custom'
    
    CHOICES = [
        (BASIC, 'Basic'),
        (PRO, 'Pro'),
        (ULTRA, 'Ultra'),
        (MEGA, 'Mega'),
        (CUSTOM, 'Custom'),
    ]

    name = models.CharField(max_length=50, choices=CHOICES)
    api_request_limit = models.IntegerField(default=0)
    rate_limit = models.IntegerField(default=0)
    token_limit = models.IntegerField(default=0)
    storage_limit = models.IntegerField(default=0)
    max_characters = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Subscription(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pricing_plan = models.ForeignKey(
        PricingPlan, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email}'s Subscription to {self.pricing_plan.name}"


class User(AbstractUser):
    id = models.CharField(max_length=100, unique=True,
                          default=uuid.uuid4, primary_key=True)
    is_developer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=True, blank=True)
    total_tokens_used = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class TokenUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    prompt_tokens_used = models.IntegerField(default=0)
    completion_tokens_used = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.month.strftime('%B %Y')}"


class SentimentAnalysis(models.Model):
    text = models.TextField()
    positive = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class EmotionAnalysis(models.Model):
    text = models.TextField()
    anger_score = models.FloatField(null=True, blank=True)
    disgust_score = models.FloatField(null=True, blank=True)
    fear_score = models.FloatField(null=True, blank=True)
    joy_score = models.FloatField(null=True, blank=True)
    neutral_score = models.FloatField(null=True, blank=True)
    sadness_score = models.FloatField(null=True, blank=True)
    surprise_score = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

# Signals
@receiver(post_save, sender=TokenUsage)
def update_token_usage(sender, instance, **kwargs):
    # Get the token usage for this subscription and month
    token_usage = instance
    prompt_tokens_used = token_usage.prompt_tokens_used
    completion_tokens_used = token_usage.completion_tokens_used
    total_tokens_used = prompt_tokens_used + completion_tokens_used

    # Update the user's API key with the new token usage information
    user = token_usage.user
    user.total_tokens_used = total_tokens_used
    user.save()
