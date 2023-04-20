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


class AIModel(BaseModel):
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.id


class PricingPlan(BaseModel):
    name = models.CharField(max_length=50)
    api_request_limit = models.IntegerField(default=0)
    rate_limit = models.IntegerField(default=0)
    token_limit = models.IntegerField(default=0)

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
    model = models.ForeignKey(
        AIModel,  null=True, blank=True, on_delete=models.CASCADE)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt_tokens_used = models.IntegerField(default=0)
    completion_tokens_used = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.month.strftime('%B %Y')}"


class Tone(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class PromptCategory(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    

class UseCase(BaseModel):
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(PromptCategory, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Prompt(BaseModel):
    description = models.TextField(null=True, blank=True)
    usecase = models.ForeignKey(
        UseCase, on_delete=models.CASCADE, blank=True, null=True)
    nov = models.IntegerField(null=True, blank=True)
    tone = models.ForeignKey(
        Tone, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def prompt(self):
        # Construct prompt using fields
        if self.nov == 1 or self.nov == None or self.nov == 0:
            return f"Please generate a {self.usecase}. The {self.usecase} should be in a {self.tone} tone and also consider the following additional information: {self.description}."
        return f"Please generate {self.nov} variations of a {self.usecase} use case. The {self.usecase} should be in a {self.tone} tone and also consider the following additional information: {self.description or 'no description provided'}. Please ensure that each {self.usecase} variation is unique and appropriate for the specified use case."


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
