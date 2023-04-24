from api.models import PricingPlan
from django.db import transaction


@transaction.atomic
def update_subscription(user, request):
    pricing_plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    rapid_api_user = request.META.get('HTTP_X_RAPIDAPI_USER')
    print('++++++++++++++++++++update subscription++++++++++++++++++')
    print(pricing_plan)
    if rapid_api_user and pricing_plan and pricing_plan != user.get_subscription():
        valid_plans = {'BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'}
        if pricing_plan in valid_plans:
            user.subscription.pricing_plan, _ = PricingPlan.objects.get_or_create(name=pricing_plan)
            user.subscription.save()
            user.first_name = rapid_api_user
            user.save()




