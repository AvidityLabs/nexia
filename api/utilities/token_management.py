from django.utils import timezone
from datetime import date
from api.models import TokenUsage


def check_count_value(val):
    return 0 if not val else val


def update_token_usage(user, prompt_tokens, completion_tokens, total_tokens, img_count=None, audio_count=None, video_count=None):
    # Get the current month and year
    today = timezone.now().date()
    month = today.month
    year = today.year

    # Get the token usage object for the current month and user, or create a new one if it doesn't exist
    token_usage, created = TokenUsage.objects.get_or_create(
        user=user,
        timestamp__month=month,
        timestamp__year=year,
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