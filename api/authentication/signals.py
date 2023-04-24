from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_started
from api.models import PricingPlan,Subscription, TokenUsage, User


@receiver(post_save, sender=User)
def create_related_subscription(sender, instance, created, *args, **kwargs):
    if created:
        pricing_plan, _ = PricingPlan.objects.get_or_create(name='PENDING')
        token_usage, _ = TokenUsage.objects.get_or_create(
            user=instance,
            pricing_plan=pricing_plan
        )
        subscription, _ = Subscription.objects.get_or_create(
            pricing_plan=pricing_plan,
            user=instance
        )
        instance.subscription = subscription
        instance.save()