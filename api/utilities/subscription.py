from api.models import Subscription,PricingPlan

def create_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    if plan in ('BASIC', 'PRO', 'ULTRA', 'MEGA', 'CUSTOM'):
        plan_obj, _ = PricingPlan.objects.get_or_create(name=plan)
        subscription = Subscription.objects.create(pricing_plan=plan_obj)
        return subscription

def get_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    pricing_plan, created = PricingPlan.objects.get_or_create(name=plan)
    if created:
        subscription = Subscription.objects.create(pricing_plan=pricing_plan)
    else:
        subscription = Subscription.objects.get(pricing_plan=pricing_plan)
    return subscription