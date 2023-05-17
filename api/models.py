from enum import Enum
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

class UseCase(Enum):
    YoutubeIdea = 1,
    YoutubeDescription = 2,
    YoutubeChannelDescription = 3,
    TestimonialAndReview = 4,
    TagLineAndHeadline = 5,
    StoryPlots = 6,
    SongLyrics = 7,
    SmsAndNotifications = 8,
    EmailSubjectLine = 9,
    JobDescription = 10,
    BlogIdeaAndOutline= 11,
    CoverLetter = 12,
    ProfileBio=13,
    ReplyToReviewsAndMessages = 14,
    GrammarCorrection = 15,
    BusinessIdea = 16,
    BusinessIdeaPitch = 17,
    Citation = 18,
    CopywritingFrameworkAIDA = 19,
    GoogleSearchAd = 20,
    InterviewQuestions = 21,
    KeywordsExtractor = 22,
    LandingPage = 23, 
    ParaphraseText = 24,
    PostAndCaptionIdea = 25,
    ProductDescriptionWithBulletPoints = 26,
    ProductDescription = 27,
    SeoMetaTitle = 28,
    GenerateCallToAction = 29,
    GenerateBrandName = 30,
    GenerateQuestionAnswer = 31,
    SocialMediaAd = 32,
    GenerateLandingPageCopy = 33,
    GenerateFacebookAd = 34,
    GenerateInstagramCaption = 35,
    GeneratePodcastIdea = 36,
    GeneratePodcastTitle = 37,
    GeneratePresentation = 38,
    GeneratePressRelease = 39,
    GenerateVideoScript = 40,
    GenerateWebsiteCopy = 41,
    GenerateNewsletterIdea = 42,
    GenerateNewsletterTitle = 43,
    GenerateSalesCopy = 44,
    GenerateCourseTitle = 45,
    GenerateCourseSubtitle = 46,
    GenerateCourseDescription = 47,
    GenerateCourseLectureTitles = 48,
    GenerateCourseQuizQuestions = 49,
    GenerateCourseExercises = 50,
    GenerateCourseArticles = 51,
    SummarizeText = 52,
    AdCopy = 53,
    EmailBody = 54,
    EmailToneAdjustment = 55,
    SocialMediaPost = 56,
    SocialMediaAdGenerator = 57,
    GoogleSearchAdsGenerator = 58,
    Email = 59

use_cases = [
    {
        'title': 'Youtube Idea',
        'description': 'Generate ideas for YouTube videos.',
        'navigateTo': UseCase.YoutubeIdea.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Youtube Description',
        'description': 'Create descriptions for YouTube videos.',
        'navigateTo': UseCase.YoutubeDescription.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Youtube Channel Description',
        'description': 'Write descriptions for YouTube channels.',
        'navigateTo': UseCase.YoutubeChannelDescription.value[0],
        'category': 'youtube'
    },
    {
        'title': 'Testimonial and Review',
        'description': 'Generate testimonials and reviews.',
        'navigateTo': UseCase.TestimonialAndReview.value[0],
        'category': 'Testimonials and Reviews'
    },
    {
        'title': 'Tagline and Headline',
        'description': 'Generate catchy taglines and headlines.',
        'navigateTo': UseCase.TagLineAndHeadline.value[0],
        'category': 'Taglines and Headlines'
    },
    {
        'title': 'Story Plots',
        'description': 'Generate plots for stories or narratives.',
        'navigateTo': UseCase.StoryPlots.value[0],
        'category': 'Story Plots'
    },
    {
        'title': 'Song Lyrics',
        'description': 'Create lyrics for songs.',
        'navigateTo': UseCase.SongLyrics.value[0],
        'category': 'Song Lyrics'
    },
    {
        'title': 'SMS and Notifications',
        'description': 'Generate text messages and notifications.',
        'navigateTo': UseCase.SmsAndNotifications.value[0],
        'category': 'SMS and Notifications'
    },
    {
        'title': 'Email Subject Line',
        'description': 'Create subject lines for emails.',
        'navigateTo': UseCase.EmailSubjectLine.value[0],
        'category': 'Email'
    },
    {
        'title': 'Job Description',
        'description': 'Write descriptions for job postings.',
        'navigateTo': UseCase.JobDescription.value[0],
        'category': 'Job-related'
    },
    {
        'title': 'Blog Idea and Outline',
        'description': 'Generate ideas and outlines for blog posts.',
        'navigateTo': UseCase.BlogIdeaAndOutline.value[0],
        'category': 'blog'
    },
    {
        'title': 'Cover Letter',
        'description': 'Create cover letters for job applications.',
        'navigateTo': UseCase.CoverLetter.value[0],
        'category': 'Job-related'
    },
    {
        'title': 'Profile Bio',
        'description': 'Write a biography for a profile or portfolio.',
        'navigateTo': UseCase.ProfileBio.value[0],
        'category': 'profile'
    },
    {
        'title': 'Reply to Reviews and Messages',
        'description': 'Craft responses to reviews and messages.',
        'navigateTo': UseCase.ReplyToReviewsAndMessages.value[0],
        'category': 'Content Creation'
    },
    {
        'title': 'Grammar Correction',
        'description': 'Correct grammar and punctuation errors.',
        'navigateTo': UseCase.GrammarCorrection.value[0],
        'category': "Business"
    },
    {
        'title': 'Business Idea',
        'description': 'Generate ideas for new businesses.',
        'navigateTo': UseCase.BusinessIdea.value[0],
        'category': 'business'
    },
    {
        'title': 'Business Idea Pitch',
        'description': 'Create a pitch for a business idea.',
        'navigateTo': UseCase.BusinessIdeaPitch.value[0],
        'category': 'business'
    },
    {
        'title': 'Citation',
        'description': 'Generate citations for references.',
        'navigateTo': UseCase.Citation.value[0],
        'category': 'academic'
    },
    {
        'title': 'Copywriting Framework AIDA',
        'description': 'Apply the AIDA framework to copywriting.',
        'navigateTo': UseCase.CopywritingFrameworkAIDA.value[0],
        'category': 'business'
    },
        {
        'title': 'Google Search Ad',
        'description': 'Generate Google search ads.',
        'navigateTo': UseCase.GoogleSearchAd.value[0],
        'category': 'Marketing and Advertising'
    },
    {
        'title': 'Interview Questions',
        'description': 'Generate interview questions.',
        'navigateTo': UseCase.InterviewQuestions.value[0],
        'category': 'Interview'
    },
    {
        'title': 'Keywords Extractor',
        'description': 'Extract keywords from text or documents.',
        'navigateTo': UseCase.KeywordsExtractor.value[0],
        'category': 'seo'
    },
    {
        'title': 'Landing Page',
        'description': 'Create landing page content.',
        'navigateTo': UseCase.LandingPage.value[0],
        'category': 'seo'
    },
    {
        'title': 'Paraphrase Text',
        'description': 'Paraphrase or rephrase text.',
        'navigateTo': UseCase.ParaphraseText.value[0],
        'category': 'Content Editing'
    },
    {
        'title': 'Post and Caption Idea',
        'description': 'Generate ideas for social media posts and captions.',
        'navigateTo': UseCase.PostAndCaptionIdea.value[0],
        'category': 'Social Media'
    },
    {
        'title': 'Product Description with Bullet Points',
        'description': 'Write product descriptions with bullet points.',
        'navigateTo': UseCase.ProductDescriptionWithBulletPoints.value[0],
        'category': 'Product Description'
    },
    {
        'title': 'Product Description',
        'description': 'Write product descriptions.',
        'navigateTo': UseCase.ProductDescription.value[0],
        'category': 'Product Description'
    },
    {
        'title': 'SEO Meta Title',
        'description': 'Generate SEO meta titles.',
        'navigateTo': UseCase.SeoMetaTitle.value[0],
        'category': 'seo'
    },
    {
        'title': 'Generate Call to Action',
        'description': 'Create compelling calls to action.',
        'navigateTo': UseCase.GenerateCallToAction.value[0],
        'category': 'Call to Action'
    },
    {
        'title': 'Generate Brand Name',
        'description': 'Generate brand names.',
        'navigateTo': UseCase.GenerateBrandName.value[0],
        'category': 'Branding'
    },
    {
        'title': 'Generate Question Answer',
        'description': 'Generate questions and answers.',
        'navigateTo': UseCase.GenerateQuestionAnswer.value[0],
        'category': 'Questions and Answers'
    },
    {
        'title': 'Social Media Ad',
        'description': 'Generate social media ads.',
        'navigateTo': UseCase.SocialMediaAd.value[0],
        'category': 'Social Media Ad Generator'
    },
    {
        'title': 'Generate Landing Page Copy',
        'description': 'Generate landing page copy.',
        'navigateTo': UseCase.GenerateLandingPageCopy.value[0],
        'category': 'Landing Page'
    },
    {
        'title': 'Generate Facebook Ad',
        'description': 'Generate Facebook ads.',
        'navigateTo': UseCase.GenerateFacebookAd.value[0],
        'category': 'Facebook Ad'
    },
    {
        'title': 'Generate Instagram Caption',
        'description': 'Generate captions for Instagram posts.',
        'navigateTo': UseCase.GenerateInstagramCaption.value[0],
        'category': 'social media'
    },
    {
        'title': 'Generate Podcast Idea',
        'description': 'Generate ideas for podcasts.',
        'navigateTo': UseCase.GeneratePodcastIdea.value[0],
        'category': 'podcast'
    },
        {
        "title": "GeneratePresentation",
        "description": "Generate engaging and visually appealing presentations for various purposes.",
        "navigateTo": "/generate-presentation",
        "category": "Presentation"
    },
    {
        "title": "GeneratePressRelease",
        "description": "Craft professional press releases to announce important news or events.",
        "navigateTo": "/generate-press-release",
        "category": "Press Release"
    },
    {
        "title": "GenerateVideoScript",
        "description": "Create compelling scripts for videos, including commercials, tutorials, or presentations.",
        "navigateTo": "/generate-video-script",
        "category": "Video Script"
    },
    {
        "title": "GenerateWebsiteCopy",
        "description": "Generate persuasive and informative copy for website pages and sections.",
        "navigateTo": "/generate-website-copy",
        "category": "Website"
    },
    {
        "title": "GenerateNewsletterIdea",
        "description": "Get creative ideas and inspiration for your newsletters.",
        "navigateTo": "/generate-newsletter-idea",
        "category": "Newsletter"
    },
    {
        "title": "GenerateNewsletterTitle",
        "description": "Generate catchy and attention-grabbing titles for your newsletters.",
        "navigateTo": "/generate-newsletter-title",
        "category": "Newsletter"
    },
    {
        "title": "GenerateSalesCopy",
        "description": "Create persuasive and compelling sales copy for marketing campaigns.",
        "navigateTo": "/generate-sales-copy",
        "category": "Sales Copy"
    },
    {
        "title": "GenerateCourseTitle",
        "description": "Generate catchy and informative titles for your online courses.",
        "navigateTo": "/generate-course-title",
        "category": "Course"
    },
    {
        "title": "GenerateCourseSubtitle",
        "description": "Craft engaging and descriptive subtitles for your online course modules.",
        "navigateTo": "/generate-course-subtitle",
        "category": "Course"
    },
    {
        "title": "GenerateCourseDescription",
        "description": "Write compelling descriptions to effectively communicate the value of your online course.",
        "navigateTo": "/generate-course-description",
        "category": "Course"
    },
    {
        "title": "GenerateCourseLectureTitles",
        "description": "Generate clear and informative titles for the lectures in your online course.",
        "navigateTo": "/generate-course-lecture-titles",
        "category": "Course"
    },
    {
        "title": "GenerateCourseQuizQuestions",
        "description": "Create engaging quiz questions to test the knowledge of your online course participants.",
        "navigateTo": "/generate-course-quiz-questions",
        "category": "Course"
    },
    {
        "title": "GenerateCourseExercises",
        "description": "Generate practical exercises to reinforce learning in your online course.",
        "navigateTo": "/generate-course-exercises",
        "category": "Course"
    },
    {
        "title": "GenerateCourseArticles",
        "description": "Generate informative articles as supplementary material for your online course.",
        "navigateTo": "/generate-course-articles",
        "category": "Course"
    },
    {
        "title": "SummarizeText",
        "description": "Summarize long pieces of text into concise and meaningful summaries.",
        "navigateTo": "/summarize-text",
        "category": "Text Summarization"
    },
        {
        "title": "AdCopy",
        "description": "Create compelling and persuasive copy for advertisements in various mediums.",
        "navigateTo": "/ad-copy",
        "category": "Ad Copy"
    },
    {
        "title": "EmailBody",
        "description": "Craft effective and engaging bodies for email communications.",
        "navigateTo": "/email-body",
        "category": "Email Body"
    },
    {
        "title": "EmailToneAdjustment",
        "description": "Adjust the tone and style of email messages to match the desired intent or audience.",
        "navigateTo": "/email-tone-adjustment",
        "category": "Email Tone Adjustment"
    },
    {
        "title": "SocialMediaPost",
        "description": "Create engaging and attention-grabbing posts for social media platforms.",
        "navigateTo": "/social-media-post",
        "category": "Social Media Post"
    },
    {
        "title": "SocialMediaAdGenerator",
        "description": "Generate effective and compelling advertisements for social media platforms.",
        "navigateTo": "/social-media-ad-generator",
        "category": "Social Media Ad Generator"
    },
    {
        "title": "GoogleSearchAdsGenerator",
        "description": "Generate ads specifically designed for Google search engine results.",
        "navigateTo": "/google-search-ads-generator",
        "category": "Google Search Ads Generator"
    }
]

# Additional use cases can be added in a similar manner

# Accessing the data:
for use_case in use_cases:
    print(use_case['title'])
    print(use_case['description'])
    print(use_case['navigateTo'])
    print()




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


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, app_owner_id=None, groups=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model.objects.filter(email=email)
        if len(user) != 0:
            raise TypeError('User email already exists.')

        user = self.model(username=email, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        if app_owner_id:
            user.app_owner_id = app_owner_id
            user.save()
        if groups:
            for group in groups:
                group_obj, _ = Group.objects.get_or_create(name=group['name'])
                user.groups.add(group_obj)
        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email)
        user.set_password(password)
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
    is_app_user = models.BooleanField(default=False)

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
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else f"Draft {self.id}"
    
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
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} Token Usage for {self.timestamp.strftime('%B %Y')}"


class SentimentAnalysis(BaseModel):
    text = models.TextField(null=True, blank=True)
    positive = models.FloatField(null=True, blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

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
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.text


class TextToImage(BaseModel):
    url = models.CharField(max_length=255)
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

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
    app_owner_id = models.CharField(max_length=255, null=True, blank=True)

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
