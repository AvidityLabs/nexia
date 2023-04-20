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
        rapid_api_key = request.META.get('X_RAPID_API_KEY', None)
        rapid_api_host = request.META.get('HTTP_X_RAPIDAPI_HOST', None)
        rapid_api_user =  request.META.get('HTTP_X_RAPIDAPI_USER', None)
        print(request.META)
        if not rapid_api_key:
            raise AuthenticationFailed('RapidAPI key not found in request headers')
        if rapid_api_host:
            raise AuthenticationFailed('RapidAPI Host not found in request headers')

        # Retrieve the user object
        try:
            user = User.objects.get(username=rapid_api_key)
        except User.DoesNotExist:
            # Create a new user if the user does not exist
            user = User.objects.create_user(
                first_name=rapid_api_user,
                username=rapid_api_key,
                email=f'{rapid_api_key}@nexia.user',
                is_developer=True,
                api_key=rapid_api_key
            )

        # Add subscription
        subscription = get_subscription(request)
        if user.subscription != subscription:
            user.subscription = subscription
            user.save()

        return (user, None)

        