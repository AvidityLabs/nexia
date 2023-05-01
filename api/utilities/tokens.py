from datetime import date
from django.utils import timezone
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from api.models import TokenUsage

from rest_framework.exceptions import APIException

class MonthlyImageLimitExceeded(APIException):
    status_code = 401
    default_detail = "Sorry, your account has exceeded the monthly image limit. Please upgrade your plan or reduce your image usage."
    default_code = "monthly_image_limit_exceeded"

class MonthlyAudioLimitExceeded(APIException):
    status_code = 401
    default_detail = "We're sorry, but you have used up your monthly audio quota. Please upgrade your plan."
    default_code = "monthly_audio_limit_exceeded"

class MonthlyVideoLimitExceeded(APIException):
    status_code = 401
    default_detail = "We regret to inform you that your monthly video limit has been exceeded. Please upgrade your plan."
    default_code = "monthly_video_limit_exceeded"

class MonthlyTokenLimitExceeded(APIException):
    status_code = 401
    default_detail = "Unfortunately, you have exceeded your monthly token limit. Please upgrade your plan."
    default_code = "monthly_token_limit_exceeded"

def check_count_value(val):
    return 0 if not val else val

# Only executed when prompting 
def update_token_usage(user, prompt_tokens, completion_tokens, total_tokens, img_count=None, audio_count=None, video_count=None):
    print('hello')
    # Get the current month and year
    today = date.today()
    month = today.month
    year = today.year

    # Get the token usage object for the current month and user, or create a new one if it doesn't exist
    token_usage, created = TokenUsage.objects.get_or_create(
        user=user,
        month=month,
        year=year,
        defaults={
            'pricing_plan': user.subscription.pricing_plan,
            'prompt_tokens_used': prompt_tokens,
            'completion_tokens_used': completion_tokens,
            'total_tokens_used': total_tokens,
            'total_images': check_count_value(img_count),
            'total_audios': check_count_value(audio_count),
            'total_videos': check_count_value(video_count)
        }
    )

    # If the token usage object already existed, update the token usage fields
    if not created:
        token_usage.prompt_tokens_used += prompt_tokens
        token_usage.completion_tokens_used += completion_tokens
        token_usage.total_tokens_used += total_tokens
        if img_count:
            token_usage.total_images += img_count
        if audio_count:
            token_usage.total_audios += audio_count
        if video_count:
            token_usage.total_videos += video_count
        token_usage.save()

# Only used on some endpoints to ckeck token usage
def validate_token_usage(user):
    # Get the user's current token usage for the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    token_usage = TokenUsage.objects.filter(user=user, month=current_month, year=current_year).first()

    if not token_usage:
        # Token usage record doesn't exist for the current month, assume no tokens used
        return {"valid": True, "message": "We couldn't find any token usage records for the current month. Please make contact support."}

    # Get the pricing plan for the user
    pricing_plan = token_usage.pricing_plan

    # Check if the user's token usage is within the limit defined in their pricing plan
    if token_usage.total_images > pricing_plan.monthly_image_limit:
        raise MonthlyImageLimitExceeded()
    if token_usage.total_audios > pricing_plan.monthly_audio_limit:
        raise MonthlyAudioLimitExceeded()
    if token_usage.total_videos > pricing_plan.monthly_video_limit:
        raise MonthlyVideoLimitExceeded()
    if token_usage.total_tokens_used > pricing_plan.monthly_token_limit:
        raise MonthlyTokenLimitExceeded()

    
    # Token usage is within the limit defined in the pricing plan
    pass

    