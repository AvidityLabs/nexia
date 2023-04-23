from datetime import datetime
from datetime import datetime
from django.utils import timezone
from api.models import Subscription,PricingPlan

def create_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    if plan in ('BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'):
        plan_obj, _ = PricingPlan.objects.get_or_create(name=plan)
        subscription = Subscription.objects.create(pricing_plan=plan_obj)
        return subscription

def get_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    pricing_plan, created = PricingPlan.objects.get_or_create(name=plan)
    if created:
        subscription = Subscription.objects.create(pricing_plan=pricing_plan)
    else:
        subscription = Subscription.objects.get(pricing_plan=pricing_plan)
    return subscription



from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from api.models import Subscription, TokenUsage, SentimentAnalysis, EmotionAnalysis

def is_subscription_valid(user):
    # Check if the user has an active subscription
    subscription = user.subscription
    if not subscription or not subscription.is_active:
        return False, _('User does not have an active subscription.')

    # Check if the subscription has expired
    if subscription.end_date and subscription.end_date < timezone.now():
        return False, _('Subscription has expired.')

    # Check if the user has exceeded the token limit
    token_usage = TokenUsage.objects.filter(user=user, timestamp__month=timezone.now().month).first()
    if token_usage and token_usage.total_tokens_used >= subscription.pricing_plan.token_limit:
        return False, _('User has exceeded the token limit for this month.')

    # Check if the user has exceeded the storage limit
    # Assuming that storage limit is the maximum number of sentiment analysis or emotion analysis objects a user can have
    sentiment_analysis_count = SentimentAnalysis.objects.filter(created_by=user).count()
    emotion_analysis_count = EmotionAnalysis.objects.filter(created_by=user).count()
    if sentiment_analysis_count + emotion_analysis_count >= subscription.pricing_plan.storage_limit:
        return False, _('User has exceeded the storage limit.')

    # Check if the user has exceeded the max characters limit
    text = "a" * (subscription.pricing_plan.max_characters + 1)
    try:
        sentiment_analysis = SentimentAnalysis(text=text, created_by=user)
        sentiment_analysis.full_clean()
        emotion_analysis = EmotionAnalysis(text=text, created_by=user)
        emotion_analysis.full_clean()
    except ValidationError:
        return False, _('User has exceeded the maximum characters limit.')

    return True, _('User subscription is valid.')
