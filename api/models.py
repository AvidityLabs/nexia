import uuid
import requests
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Group,  PermissionsMixin
)

from django.db import models
import jwt
import cloudinary.uploader
from cloudinary.models import CloudinaryField

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

    name = models.CharField(max_length=50, choices=CHOICES, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    features = models.TextField(null=True,blank=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, default="0.00")
    monthly_character_limit = models.IntegerField(default=0)
    monthly_image_limit = models.IntegerField(default=0)
    monthly_audio_limit = models.IntegerField(default=0)
    monthly_video_limit = models.IntegerField(default=0)
    monthly_rate_limit = models.IntegerField(default=0)
    monthly_data_storage_limit = models.IntegerField(default=0)
    monthly_token_limit = models.IntegerField(default=0)
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
    username = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.pricing_plan:
            return f"{self.pricing_plan.name}"
        return ''

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None, roles=None, app_owner_id=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')
        
        user = self.model.objects.filter(email=email)
        if len(user) !=0:
            raise TypeError('User email already exists.')
        
        if len(self.model.objects.filter(username=username))!=0:
            raise TypeError('Username already exists.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        if app_owner_id:
            user.app_owner_id=app_owner_id
            user.save()
        return user


    
    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=100, unique=True,
                          default=uuid.uuid4, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_developer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=True, blank=True)
    total_tokens_used = models.IntegerField(default=0)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')
    is_app_user = models.BooleanField(default=False)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
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

class TokenUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, null=True,blank=True)
    prompt_tokens_used = models.IntegerField(default=0)
    completion_tokens_used = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)
    total_images = models.IntegerField(default=0)
    total_audios = models.IntegerField(default=0)
    total_videos = models.IntegerField(default=0)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.timestamp.strftime('%B %Y')}"


class SentimentAnalysis(models.Model):
    text = models.TextField(null=True, blank=True)
    positive = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.text

class EmotionAnalysis(models.Model):
    text = models.TextField(null=True, blank=True)
    anger_score = models.FloatField(null=True, blank=True)
    disgust_score = models.FloatField(null=True, blank=True)
    fear_score = models.FloatField(null=True, blank=True)
    joy_score = models.FloatField(null=True, blank=True)
    neutral_score = models.FloatField(null=True, blank=True)
    sadness_score = models.FloatField(null=True, blank=True)
    surprise_score = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.text


class TextToImage(models.Model):
    image = models.CharField(max_length=255)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def generate_image(self, text):
        # Call the AI API to generate the image based on the input text
        response = requests.post('https://your-ai-api.com/generate-image', json={'text': text})

        # Upload the generated image to Cloudinary
        upload_result = cloudinary.uploader.upload(response.content)

        # Save the Cloudinary URL to the Django model
        self.image = upload_result['url']
        self.save()

class TextToVideo(models.Model):
    video = models.CharField(max_length=255)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def generate_video(self, text):
        # Call the AI API to generate the video based on the input text
        response = requests.post('https://your-ai-api.com/generate-video', json={'text': text})

        # Upload the generated video to Cloudinary
        upload_result = cloudinary.uploader.upload(response.content, resource_type="video")

        # Save the Cloudinary URL to the Django model
        self.video = upload_result['url']
        self.save()


class Tone(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name
    
class InstructionCategory(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name
    
class Instruction(BaseModel):
     description = models.TextField(null=True, blank=True)
     tones = models.ManyToManyField(Tone,blank=True)
     nov = models.IntegerField(null=True, blank=True)
     category = models.ForeignKey(InstructionCategory, on_delete=models.CASCADE, null=True, blank=True)
        
     @property
     def prompt(self):
        tones = ""
        for t in self.tones.all():
            tones+=t.name
        return f"Please {self.description}. The text should be written in a {tones} tone. The text is for {self.category.name} purposes"

