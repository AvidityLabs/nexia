from django.contrib import admin
from .models import PricingPlan, Subscription, User, TokenUsage, SentimentAnalysis, EmotionAnalysis

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_request_limit', 'rate_limit', 'token_limit', 'storage_limit')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricing_plan', 'start_date', 'end_date', 'is_active')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_developer', 'is_admin', 'is_superuser', 'api_key', 'subscription', 'total_tokens_used')

@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'pricing_plan', 'prompt_tokens_used', 'completion_tokens_used', 'total_tokens_used', 'timestamp')

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('text', 'positive', 'analyzed_at')

@admin.register(EmotionAnalysis)
class EmotionAnalysisAdmin(admin.ModelAdmin):
    list_display = ('text', 'anger_score', 'disgust_score', 'fear_score', 'joy_score', 'neutral_score', 'sadness_score', 'surprise_score', 'analyzed_at')
