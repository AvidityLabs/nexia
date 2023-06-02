"""
models.py - Contains the database models for the application.

Author: Philip Mutua
Email: pmutua@live.com
"""

import uuid
from datetime import datetime, timedelta
import requests
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
import jwt
import cloudinary.uploader
from cloudinary.models import CloudinaryField

AUTH_PROVIDERS = {
    'email': 'email',
    'facebook.com': 'facebook.com',
    'google.com': 'google.com',
    'twitter.com': 'twitter.com'
}


class BaseModel(models.Model):
    """
    A base model representing common attributes shared by other models.

    Attributes:
        created_at (DateTimeField): The date and time when the object was created.
        updated_at (DateTimeField): The date and time when the object was last updated.
        deleted_at (DateTimeField): The date and time when the object was deleted (if applicable).
        created_by (CharField): The user who created the object.

    Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Language(models.Model):
    """
    A model representing supported languages.

    Attributes:
        name (CharField): The name of the language.
        code (CharField): The code representing the language.

    Methods:
        __str__(): Returns a string representation of the language.

    """

    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the language.
        """
        return self.name


class PricingPlan(BaseModel):
    """
    Model representing a pricing plan.

    Attributes:
        BASIC (str): Constant for the 'BASIC' plan.
        PRO (str): Constant for the 'PRO' plan.
        ULTRA (str): Constant for the 'ULTRA' plan.
        MEGA (str): Constant for the 'MEGA' plan.
        CUSTOM (str): Constant for the 'CUSTOM' plan.
        PENDING (str): Constant for the 'PENDING' plan.
        MONTHLY (str): Constant for the 'monthly' duration.
        YEARLY (str): Constant for the 'yearly' duration.
        CHOICES (list): List of available plan choices.
        DURATION_CHOICES (list): List of available duration choices.

        name (CharField): Name of the pricing plan.
        description (TextField): Description of the pricing plan.
        features (TextField): Features of the pricing plan.
        monthly_price (DecimalField): Monthly price of the plan.
        yearly_price (DecimalField): Yearly price of the plan.
        duration (CharField): Duration of the plan.
        monthly_character_limit (IntegerField): Monthly character limit.
        monthly_image_limit (IntegerField): Monthly image limit.
        monthly_audio_limit (IntegerField): Monthly audio limit.
        monthly_video_limit (IntegerField): Monthly video limit.
        monthly_rate_limit (IntegerField): Monthly rate limit.
        monthly_data_storage_limit (IntegerField): Monthly data storage limit.
        monthly_token_limit (IntegerField): Monthly token limit.
        additional_character_charge (DecimalField): Additional character charge.
        currency (CharField): Currency used for the plan.

    Methods:
        __str__(): Returns the name of the pricing plan.
    """

    BASIC = 'BASIC'
    PRO = 'PRO'
    ULTRA = 'ULTRA'
    MEGA = 'MEGA'
    CUSTOM = 'CUSTOM'
    PENDING = 'PENDING'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

    CHOICES = [
        (BASIC, 'BASIC'),
        (PRO, 'PRO'),
        (ULTRA, 'ULTRA'),
        (MEGA, 'MEGA'),
        (CUSTOM, 'CUSTOM'),
        (PENDING, 'PENDING'),
    ]

    DURATION_CHOICES = [
        (MONTHLY, 'monthly'),
        (YEARLY, 'yearly'),
    ]

    name = models.CharField(
        max_length=50, choices=CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    monthly_price = models.DecimalField(
        max_digits=8, decimal_places=2, default="0.00")
    yearly_price = models.DecimalField(
        max_digits=8, decimal_places=2, default="0.00")
    duration = models.CharField(
        max_length=50, choices=DURATION_CHOICES, null=True, blank=True)
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
        """
        Returns the name of the pricing plan.

        Returns:
            str: The name of the pricing plan.
        """
        return self.name


class Subscription(BaseModel):
    """
    Represents a subscription.

    Attributes:
        id (UUIDField): The unique identifier for the subscription (primary key).
        pricing_plan (ForeignKey): The associated pricing plan for the subscription.
        start_date (DateTimeField): The date and time when the subscription started.
        end_date (DateTimeField): The date and time when the subscription ends (nullable).
        is_active (BooleanField): Indicates whether the subscription is active or not.
        username (CharField): The username associated with the subscription (nullable).
        user_id (CharField): The user ID associated with the subscription (nullable).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pricing_plan = models.ForeignKey(
        PricingPlan, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """
        Returns the name of the associated pricing plan.

        Returns:
            str: The name of the associated pricing plan.
        """
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

    def create_user(self, email, password=None, pricing_plan=None, display_name=None, photo_url=None, uid=None, auth_provider=None, is_verified=None):
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
            is_verified=is_verified,
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
    """
    Represents a user.

    Attributes:
        id (CharField): The unique identifier for the user.
        email (EmailField): The email address of the user (unique).
        username (CharField): The username of the user (nullable, unique).
        display_name (CharField): The display name of the user (nullable).
        photo_url (TextField): The URL of the user's photo (nullable).
        phone_number (CharField): The phone number of the user (nullable).
        bio (TextField): The bio of the user (nullable).
        is_admin (BooleanField): Indicates whether the user is an admin or not.
        is_superuser (BooleanField): Indicates whether the user is a superuser or not.
        is_staff (BooleanField): Indicates whether the user is staff or not.
        is_verified (BooleanField): Indicates whether the user is verified or not.
        uid (CharField): The UID of the user (nullable).
        pricing_plan (CharField): The pricing plan of the user (nullable).
        subscription (ForeignKey): The associated subscription for the user (nullable).
        total_tokens_used (IntegerField): The total number of tokens used by the user.
        auth_provider (CharField): The authentication provider for the user (nullable).

    Additional attributes:
        USERNAME_FIELD (str): The field used for logging in (set to 'username').
        REQUIRED_FIELDS (list): The required fields for creating a user (set to ['email']).
    """

    id = models.CharField(max_length=100, unique=True,
                          default=uuid.uuid4, primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
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
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=True, blank=True)
    total_tokens_used = models.IntegerField(default=0)
    auth_provider = models.CharField(
        blank=True, null=True, max_length=20, default=AUTH_PROVIDERS.get('email'))

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
    """
    Represents a category for use cases.

    Attributes:
        name (CharField): The name of the category (nullable).

    Methods:
        __str__(): Returns the name of the category.
    """

    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class UseCase(BaseModel):
    """
    Represents a use case.

    Attributes:
        title (CharField): The title of the use case (nullable).
        description (TextField): The description of the use case (nullable).
        navigateTo (CharField): The navigation link for the use case (nullable).
        category (ForeignKey): The associated category for the use case (nullable).

    Methods:
        __str__(): Returns the title of the use case.
    """

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    navigateTo = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        UseCaseCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class DraftManager(models.Manager):
    def favourites(self, **kwargs):
        """Draft.objects.favourites().count()"""
        return self.filter(created_at__lte=timezone.now(), **kwargs)


class Draft(BaseModel):
    """
    Represents a draft of a use case.

    Attributes:
        user (ForeignKey): The user associated with the draft (nullable).
        use_case (ForeignKey): The use case associated with the draft (nullable).
        title (CharField): The title of the draft (nullable).
        content (TextField): The content of the draft (nullable).
        is_saved (BooleanField): Indicates whether the draft is saved or not (default: False).
        is_favourite (BooleanField): Indicates whether the draft is marked as a favorite or not (default: False).

    Methods:
        __str__(): Returns the title of the draft or a default string if the title is not available.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    use_case = models.ForeignKey(
        UseCase, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_saved = models.BooleanField(default=False)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.title if self.title else f"Draft {self.id}"

    objects = DraftManager()


class TokenUsageManager(models.Manager):
    """
    Custom manager for TokenUsage model.

    Methods:
        get_yearly_token_usage(user, year): Retrieves the yearly token usage data for a specific user.
    """

    def get_yearly_token_usage(self, user, year):
        """
        Retrieves the yearly token usage data for a specific user.

        Args:
            user (User): The user for whom to retrieve the token usage data.
            year (int): The year for which to retrieve the token usage data.

        Returns:
            dict: A dictionary containing the year and monthly token usage values.
        """
        # Filter TokenUsage objects for the user and year
        token_usage_data = self.filter(user=user, year=year).order_by('month')

        # Extract the monthly token usage values
        monthly_token_usage = [
            token.total_tokens_used for token in token_usage_data]

        return {
            "year": year,
            "token_usage": monthly_token_usage,
        }


class TokenUsage(models.Model):
    """
    Represents the usage of tokens by a user.

    Attributes:
        user (ForeignKey): The user associated with the token usage (nullable).
        pricing_plan (ForeignKey): The pricing plan associated with the token usage (nullable).
        prompt_tokens_used (IntegerField): The number of prompt tokens used.
        completion_tokens_used (IntegerField): The number of completion tokens used.
        total_tokens_used (IntegerField): The total number of tokens used.
        total_images (IntegerField): The total number of images used.
        total_audios (IntegerField): The total number of audios used.
        total_videos (IntegerField): The total number of videos used.
        month (IntegerField): The month of the token usage (nullable).
        year (IntegerField): The year of the token usage (nullable).
        timestamp (DateTimeField): The timestamp of when the token usage was recorded.

    Methods:
        __str__(): Returns a string representation of the token usage.
        get_yearly_token_usage(user, year): Retrieves the yearly token usage data for a specific user.
    """

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
        """
        Returns a string representation of the token usage.

        Returns:
            str: The string representation of the token usage.
        """
        return f"{self.user.email} Token Usage for {self.timestamp.strftime('%B %Y')}"

    @staticmethod
    def get_yearly_token_usage(user, year):
        """
        Retrieves the yearly token usage data for a specific user.

        Args:
            user (User): The user for whom to retrieve the token usage data.
            year (int): The year for which to retrieve the token usage data.

        Returns:
            dict: A dictionary containing the year and monthly token usage values.
        """
        # Filter TokenUsage objects for the user and year
        token_usage_data = TokenUsage.objects.filter(
            user=user, year=year).order_by('month')

        # Extract the monthly token usage values and month labels
        monthly_token_usage = [
            token.total_tokens_used for token in token_usage_data]

        return {
            "year": year,
            "token_usage": monthly_token_usage,
        }


class SentimentAnalysis(BaseModel):
    """
    Represents the sentiment analysis of a piece of text.

    Attributes:
        text (TextField): The text to be analyzed.
        positive (FloatField): The positivity score of the text.
        analyzed_at (DateTimeField): The timestamp of when the analysis was performed.

    Methods:
        __str__(): Returns a string representation of the sentiment analysis.
    """

    text = models.TextField(null=True, blank=True)
    positive = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the sentiment analysis.

        Returns:
            str: The string representation of the sentiment analysis.
        """
        return self.text


class EmotionAnalysis(BaseModel):
    """
    Represents the emotion analysis of a piece of text.

    Attributes:
        text (TextField): The text to be analyzed.
        anger_score (FloatField): The anger score of the text.
        disgust_score (FloatField): The disgust score of the text.
        fear_score (FloatField): The fear score of the text.
        joy_score (FloatField): The joy score of the text.
        neutral_score (FloatField): The neutral score of the text.
        sadness_score (FloatField): The sadness score of the text.
        surprise_score (FloatField): The surprise score of the text.
        analyzed_at (DateTimeField): The timestamp of when the analysis was performed.

    Methods:
        __str__(): Returns a string representation of the emotion analysis.
    """

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
        """
        Returns a string representation of the emotion analysis.

        Returns:
            str: The string representation of the emotion analysis.
        """
        return self.text


class TextToImage(BaseModel):
    """
    Represents a text-to-image conversion.

    Attributes:
        url (CharField): The URL of the generated image.

    Methods:
        generate_image(text): Generates an image based on the input text.
    """

    url = models.CharField(max_length=255)

    def generate_image(self, text):
        """
        Generates an image based on the input text.

        Args:
            text (str): The input text to generate the image.

        Returns:
            None
        """
        # Call the AI API to generate the image based on the input text
        response = requests.post(
            'https://your-ai-api.com/generate-image', json={'text': text})

        # Upload the generated image to Cloudinary
        upload_result = cloudinary.uploader.upload(response.content)

        # Save the Cloudinary URL to the Django model
        self.url = upload_result['url']
        self.save()


class TextToVideo(BaseModel):
    """
    Represents a text-to-video conversion.

    Attributes:
        url (CharField): The URL of the generated video.

    Methods:
        generate_video(text): Generates a video based on the input text.
    """

    url = models.CharField(max_length=255)

    def generate_video(self, text):
        """
        Generates a video based on the input text.

        Args:
            text (str): The input text to generate the video.

        Returns:
            None
        """
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
    """
    Represents a tone.

    Attributes:
        name (CharField): The name of the tone.

    Methods:
        __str__(): Returns a string representation of the tone.
    """

    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the tone.

        Returns:
            str: The name of the tone.
        """
        return self.name


class Instruction(BaseModel):
    """
    Represents an instruction for generating a prompt.

    Attributes:
        description (TextField): The description of the instruction.
        tones (ManyToManyField): The tones associated with the instruction.
        audience (CharField): The intended audience for the prompt.
        style (CharField): The writing style for the prompt.
        context (CharField): The context for the prompt.
        language (CharField): The language of the prompt.
        length (CharField): The length of the prompt.
        source_text (CharField): The source text for the prompt.

    Methods:
        generate_prompt(): Generates a prompt based on the instruction attributes.
        prompt (property): Returns the generated prompt based on the instruction attributes.
    """

    description = models.TextField(null=True, blank=True)
    tones = models.ManyToManyField(Tone, blank=True)
    audience = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=100, blank=True, null=True)
    context = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    length = models.CharField(max_length=100, blank=True, null=True)
    source_text = models.CharField(max_length=100, blank=True, null=True)

    def generate_prompt(self, description, audience, style, context, language, length, source_text, tones):
        """
        Generates a prompt based on the instruction attributes.

        Args:
            description (str): The description of the instruction.
            audience (str): The intended audience for the prompt.
            style (str): The writing style for the prompt.
            context (str): The context for the prompt.
            language (str): The language of the prompt.
            length (str): The length of the prompt.
            source_text (str): The source text for the prompt.
            tones (str): The tones associated with the instruction.

        Returns:
            str: The generated prompt.
        """

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
        """
        Returns the generated prompt based on the instruction attributes.

        Returns:
            str: The generated prompt.
        """

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
