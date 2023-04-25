from datetime import date
from api.models import PricingPlan, TokenUsage, Subscription
from django.db import transaction


@transaction.atomic
def update_subscription(user, request):
    pricing_plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    rapid_api_user = request.META.get('HTTP_X_RAPIDAPI_USER')

    if rapid_api_user and pricing_plan and pricing_plan != user.get_subscription():
        valid_plans = {'BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'}
        if pricing_plan in valid_plans:
            pricing_plan_obj, _ = PricingPlan.objects.get_or_create(name=pricing_plan)

            # NOTE: subscription will always be created by default using signals.
            # update subscription info
            user.subscription.pricing_plan = pricing_plan_obj
            user.subscription.username = rapid_api_user
            user.subscription.save()
            user.first_name = rapid_api_user
            user.created_by= rapid_api_user
            user.save()

            # update token usage object
            today = date.today()
            token_usage = TokenUsage.objects.filter(
                user=user,
                month=today.month,
                year=today.year,
            ).first()

            if token_usage:
                token_usage.pricing_plan = pricing_plan_obj
                token_usage.save()
            else:
                token_usage = TokenUsage(
                    user=user,
                    month=today.month,
                    year=today.year,
                    pricing_plan=pricing_plan_obj,
                )
                token_usage.save()
                 
            







