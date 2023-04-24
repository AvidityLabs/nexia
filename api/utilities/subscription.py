from datetime import date
from api.models import PricingPlan, TokenUsage
from django.db import transaction


@transaction.atomic
def update_subscription(user, request):
    pricing_plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    rapid_api_user = request.META.get('HTTP_X_RAPIDAPI_USER')
    if rapid_api_user and pricing_plan and pricing_plan != user.get_subscription():
        valid_plans = {'BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'}
        if pricing_plan in valid_plans:
            pricing_plan_obj, _ = PricingPlan.objects.get_or_create(name=pricing_plan)
            user.subscription.pricing_plan = pricing_plan_obj
            user.subscription.save()
            user.first_name = rapid_api_user
            user.save()

            # Get token usage for the month 
            today = date.today()
            token_usage, _ = TokenUsage.objects.get_or_create(
                user=user,
                month=today.month,
                year=today.year,
                defaults={'pricing_plan': pricing_plan_obj}
            )
            token_usage.pricing_plan = pricing_plan_obj
            token_usage.save()
                 
            







