import uuid
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
import jwt


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

    name = models.CharField(max_length=50, choices=CHOICES, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    features = models.TextField(null=True,blank=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, default="0.00")
    monthly_character_limit = models.IntegerField(default=0)
    rate_limit = models.IntegerField(default=0)
    data_storage_limit = models.IntegerField(default=0)
    additional_character_charge = models.DecimalField(max_digits=8, decimal_places=4, default="0.00")
    currency = models.CharField(max_length=3, default='USD')


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


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None, request=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_user_subscription(self, user_id, request):
        """
        Create a subscription for the user with the given user_id and return the user object.
        """
        if request is None:
            raise TypeError('A valid request object is required to create a subscription.')
            
        user = self.model.objects.filter(id=user_id).first()
        if user is None:
            raise ValueError('User with id={} does not exist.'.format(user_id))
        
        plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
        if plan not in ('BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'):
            raise ValueError('Invalid subscription plan: {}'.format(plan))
        
        plan_obj, _ = PricingPlan.objects.get_or_create(name=plan)
        subscription = Subscription.objects.create(pricing_plan=plan_obj)
        user.subscription = subscription
        user.save()
        return user


        
            

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=100, unique=True,
                          default=uuid.uuid4, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_developer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=True, blank=True)
    total_tokens_used = models.IntegerField(default=0)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token


class TokenUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE)
    prompt_tokens_used = models.IntegerField(default=0)
    completion_tokens_used = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.timestamp.strftime('%B %Y')}"


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

"""_summary_
Yes, the signal post_save is used to update the user's total_tokens_used field whenever a new TokenUsage instance is created or an existing one is updated. This signal is triggered whenever a TokenUsage object is saved, which allows us to keep track of the user's token usage on an ongoing basis. The update_token_usage function receives the TokenUsage instance as an argument, and calculates the total number of tokens used by the user based on the prompt_tokens_used and completion_tokens_used fields of the TokenUsage instance. It then updates the user's total_tokens_used field with this new information. This signal ensures that the user's token usage is always up-to-date, and provides a way to track token usage on a month-to-month basis.
"""
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
