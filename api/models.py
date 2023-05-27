import uuid
from datetime import date
from django.utils import timezone
import json 
import requests
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Group,  PermissionsMixin
)


from django.db import models
import jwt
import cloudinary.uploader
from cloudinary.models import CloudinaryField

AUTH_PROVIDERS = {
    'email':'email',
    'facebook.com': 'facebook.com',
    'google.com': 'google.com',
    'twitter.com': 'twitter.com' 
}

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class PricingPlan(BaseModel):
    BASIC = 'BASIC'
    PRO = 'PRO'
    ULTRA = 'ULTRA'
    MEGA = 'MEGA'
    CUSTOM = 'CUSTOM'
    PENDING = 'PENDING'

    CHOICES = [
        (BASIC, 'BASIC'),
        (PRO, 'PRO'),
        (ULTRA, 'ULTRA'),
        (MEGA, 'MEGA'),
        (CUSTOM, 'CUSTOM'),
        (PENDING, 'PENDING'),
    ]

    name = models.CharField(
        max_length=50, choices=CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    monthly_price = models.DecimalField(
        max_digits=8, decimal_places=2, default="0.00")
    monthly_character_limit = models.IntegerField(default=0)
    monthly_image_limit = models.IntegerField(default=0)
    monthly_audio_limit = models.IntegerField(default=0)
    monthly_video_limit = models.IntegerField(default=0)
    monthly_rate_limit = models.IntegerField(default=0)
    monthly_data_storage_limit = models.IntegerField(default=0)
    monthly_token_limit = models.IntegerField(default=0)
    additional_character_charge = models.DecimalField(
        max_digits=8, decimal_places=4, default="0.00")
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.pricing_plan:
            return f"{self.pricing_plan.name}"
        return ''


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, pricing_plan=None, display_name=None, photo_url=None, uid=None, auth_provider=None,is_verified=None):
        """Create and return a `User` with an email, username, and password."""
        provider = auth_provider or 'email'
        plan = pricing_plan or 'BASIC'
        display_name = display_name or ''
        photo_url = photo_url or ''
        uid = uid or ''
        is_verified = is_verified or True

        if not email:
            raise TypeError('Users must have an email address.')

        if self.model.objects.filter(email=email).exists():
            raise TypeError('User email already exists.')

        user = self.model(
            username=email,
            email=self.normalize_email(email),
            display_name=display_name,
            photo_url=photo_url,
            uid=uid,
            pricing_plan=plan,
            is_verified= is_verified,
            auth_provider=provider
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=100, unique=True,
                          default=uuid.uuid4, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    uid = models.CharField(max_length=20, null=True, blank=True)
    pricing_plan = models.CharField(max_length=20, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    total_tokens_used = models.IntegerField(default=0)
    auth_provider = models.CharField(blank=True,null=True,max_length=20, default=AUTH_PROVIDERS.get('email'))

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        if self.subscription is None:
            return f'{self.email}'
        else:
            return f'{self.email} - Subscription Plan= {self.subscription.pricing_plan} - Tokens Used = {self.total_tokens_used}'

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_subscription(self):
        """
        This method is used to get the user subscription
        """
        plan = self.subscription.pricing_plan.name
        return plan

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        exp_timestamp = int(dt.timestamp())

        token = jwt.encode({
            'id': str(self.pk),
            'exp': exp_timestamp
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

class UseCaseCategory(BaseModel):
    name =  models.CharField(max_length=255,blank=True, null=True) 

def __str__(self):
    return self.name

class UseCase(BaseModel):
    title = models.CharField(max_length=255,blank=True, null=True) 
    description = models.TextField(blank=True, null=True)
    navigateTo = models.CharField(max_length=255,blank=True, null=True) 
    category = models.ForeignKey(UseCaseCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Draft(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    use_case = models.ForeignKey(UseCase, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.title if self.title else f"Draft {self.id}"
  
class TokenUsageManager(models.Manager):
    def get_yearly_token_usage(self, user, year):
        # Filter TokenUsage objects for the user and year
        token_usage_data = self.filter(user=user, year=year).order_by('month')

        # Extract the monthly token usage values
        monthly_token_usage = [token.total_tokens_used for token in token_usage_data]

        return {
            "year": year,
            "token_usage": monthly_token_usage,
        }  
class TokenUsage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    pricing_plan = models.ForeignKey(
        PricingPlan, on_delete=models.CASCADE, null=True, blank=True)
    prompt_tokens_used = models.IntegerField(default=0)
    completion_tokens_used = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)
    total_images = models.IntegerField(default=0)
    total_audios = models.IntegerField(default=0)
    total_videos = models.IntegerField(default=0)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = TokenUsageManager()

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.timestamp.strftime('%B %Y')}"
    
    def get_yearly_token_usage(user, year):
        # Filter TokenUsage objects for the user and year
        token_usage_data = TokenUsage.objects.filter(user=user, year=year).order_by('month')

        # Extract the monthly token usage values and month labels
        monthly_token_usage = [token.total_tokens_used for token in token_usage_data]

        return {
            "year": year,
            "token_usage": monthly_token_usage,
        }


class SentimentAnalysis(BaseModel):
    text = models.TextField(null=True, blank=True)
    positive = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class EmotionAnalysis(BaseModel):
    text = models.TextField(null=True, blank=True)
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


class TextToImage(BaseModel):
    url = models.CharField(max_length=255)

    def generate_image(self, text):
        # Call the AI API to generate the image based on the input text
        response = requests.post(
            'https://your-ai-api.com/generate-image', json={'text': text})

        # Upload the generated image to Cloudinary
        upload_result = cloudinary.uploader.upload(response.content)

        # Save the Cloudinary URL to the Django model
        self.im = upload_result['url']
        self.save()


class TextToVideo(BaseModel):
    url = models.CharField(max_length=255)

    def generate_video(self, text):
        # Call the AI API to generate the video based on the input text
        response = requests.post(
            'https://your-ai-api.com/generate-video', json={'text': text})

        # Upload the generated video to Cloudinary
        upload_result = cloudinary.uploader.upload(
            response.content, resource_type="video")

        # Save the Cloudinary URL to the Django model
        self.url = upload_result['url']
        self.save()


class Tone(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Instruction(BaseModel):
    description = models.TextField(null=True, blank=True)
    tones = models.ManyToManyField(Tone, blank=True)
    audience = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=100, blank=True, null=True)
    context = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    length = models.CharField(max_length=100, blank=True, null=True)
    source_text = models.CharField(max_length=100, blank=True, null=True)

    def generate_prompt(self,description, audience, style, context, language, length, source_text, tones):
        prompt = f"Write a {tones} prompt"
        if description:
            prompt += f" about {description}."
        else:
            prompt += "."
        if audience:
            prompt += f" The intended audience is {audience}."
        if style:
            prompt += f" The writing style should be {style}."
        if context:
            prompt += f" The prompt should be set in the context of {context}."
        if language:
            prompt += f" The prompt should be in {language}."
        if length:
            prompt += f" The prompt should be {length} in length."
        if source_text:
            prompt += f" The prompt should be based on the source text {source_text}."

        return prompt


    @property
    def prompt(self):
        tones = '/'.join(i.name for i in self.tones.all())
        return self.generate_prompt(
            self.description,
            self.audience,
            self.style,
            self.context,
            self.language,
            self.length,
            self.source_text,
            tones)
