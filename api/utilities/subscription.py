from datetime import datetime
from datetime import datetime
from django.utils import timezone
from api.models import Subscription,PricingPlan

def update_subscription(user, request):
    pricing_plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION', None)
    current_subscription = user.get_subscription()
    if pricing_plan and current_subscription and pricing_plan != current_subscription:
        valid_plans = ('BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM')        
        if pricing_plan in valid_plans:
            plan_obj, _ = PricingPlan.objects.get_or_create(name=pricing_plan)
            user.subscription.pricing_plan = plan_obj


