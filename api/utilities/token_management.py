from django.utils import timezone
from datetime import date
from api.models import TokenUsage


def update_token_usage(user, prompt_tokens, completion_tokens, total_tokens):
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
        }
    )
    
    # If the token usage object already existed, update the token usage fields
    if not created:
        token_usage.prompt_tokens_used += prompt_tokens
        token_usage.completion_tokens_used += completion_tokens
        token_usage.total_tokens_used += total_tokens
        token_usage.save()