from api.models import PricingPlan, Subscription, TokenUsage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import F, Sum

User = get_user_model()


@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        today = timezone.now().date()
        pricing_plan_instance, _ = PricingPlan.objects.get_or_create(
            name=instance.pricing_plan)
        subscription = Subscription.objects.create(
            user_id=instance.id,
            pricing_plan=pricing_plan_instance,
            username=instance.username
        )
        TokenUsage.objects.create(
            pricing_plan=pricing_plan_instance,
            user=instance,
            month=today.month,
            year=today.year
        )
        instance.subscription = subscription
        instance.save()
    else:
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year

        # Check if a token usage object exists for the current month and year
        token_usage = TokenUsage.objects.filter(
            user=instance, month=current_month, year=current_year).exists()

        if not token_usage:
            pricing_plan_instance, _ = PricingPlan.objects.get_or_create(
                name=instance.pricing_plan)

            TokenUsage.objects.create(
                pricing_plan=pricing_plan_instance,
                user=instance,
                month=current_month,
                year=current_year
            )
