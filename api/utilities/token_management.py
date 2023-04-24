from django.db.models import F
from api.models import TokenUsage

def update_token_usage(user, prompt_tokens, completion_tokens, total_tokens):
    print('-------------------------------------')
    tokenusage_obj, _ = TokenUsage.objects.get_or_create(
        user=user,
        defaults={
            'pricing_plan': user.subscription.pricing_plan,
            'prompt_tokens_used': prompt_tokens,
            'completion_tokens_used': completion_tokens,
            'total_tokens_used': total_tokens,
        }
    )
    print(tokenusage_obj)

    print('-------------------------------------')

    # Update the TokenUsage object for the current month
    tokenusage_obj.total_tokens_used = F('total_tokens_used') + total_tokens
    tokenusage_obj.save(update_fields=['total_tokens_used'])
