import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User, PricingPlan, Subscription






def get_subscription(request):
    plan = request.META.get('HTTP_X_RAPIDAPI_SUBSCRIPTION')
    pricing_plan, created = PricingPlan.objects.get_or_create(name=plan)
    if created:
        subscription = Subscription.objects.create(pricing_plan=pricing_plan)
    else:
        subscription = Subscription.objects.get(pricing_plan=pricing_plan)
    return subscription


class RapidAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the user's RapidAPI key from the request header
        authorization_key = request.META.get('HTTP_AUTHORIZATION', None)
        rapid_api_host = request.META.get('HTTP_X_RAPIDAPI_HOST', None)

        if not authorization_key:
            raise AuthenticationFailed('Authorization key not found in request headers')
        if rapid_api_host:
            raise AuthenticationFailed('RapidAPI Host not found in request headers')

        # Retrieve the user object
        try:
            user = User.objects.get(developer_id=authorization_key)
            # Add subscription
            subscription = get_subscription(request)
            if user.subscription != subscription:
                user.subscription = subscription
                user.save()
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not registered')



        

        