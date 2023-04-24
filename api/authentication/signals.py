from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_started
from api.models import TokenUsage, User


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

