from datetime import datetime
from datetime import datetime
from django.utils import timezone
from api.models import Subscription,PricingPlan

def update_subscription(user, request):
    pricing_plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')

    current_subscription = user.get_subscription()
    if pricing_plan and current_subscription:
        if pricing_plan in ('BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'):
            plan_obj, _ = PricingPlan.objects.get_or_create(name=pricing_plan)
            if current_subscription != pricing_plan:
                plan, _ = PricingPlan.objects.get_or_create(pricing_plan)
                user.subscription.plan=plan
                user.save()
            subscription = Subscription.objects.create(pricing_plan=plan_obj)
            return subscription

