from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_started
from api.models import PricingPlan,Subscription, TokenUsage, User


@receiver(post_save, sender=User)
def create_related_subscription(sender, instance, created, *args, **kwargs):
    today = date.today()
    if created:
        pricing_plan, _ = PricingPlan.objects.get_or_create(name='NOTSET')
        subscription, _ = Subscription.objects.get_or_create(
            user_id=instance.id,
            pricing_plan=pricing_plan,
        )
        instance.subscription = subscription
        instance.save()
        token_usage, _ = TokenUsage.objects.get_or_create(
            pricing_plan=pricing_plan,
            user=instance,
            month=today.month,
            year=today.year
        )