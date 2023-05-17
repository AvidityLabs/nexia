from django.contrib import admin
from .models import Instruction, PricingPlan, Subscription, User, TokenUsage, SentimentAnalysis, EmotionAnalysis, Tone

admin.site.register(Tone)

admin.site.register(Instruction)

admin.site.register(PricingPlan)

# @admin.register(PricingPlan)
# class PricingPlanAdmin(admin.ModelAdmin):
#     list_display = ('name', 'monthly_price','monthly_token_limit', 'monthly_character_limit', 'monthly_rate_limit', 'monthly_data_storage_limit', 'monthly_image_limit','monthly_audio_limit','monthly_video_limit')
#     list_filter = ('name',)
#     search_fields = ('name',)
#     ordering = ('name',)
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'description', 'features')
#         }),
#         ('Pricing Details', {
#             'fields': ('monthly_price', 'currency','monthly_token_limit', 'monthly_character_limit', 'monthly_rate_limit', 'monthly_data_storage_limit', 'monthly_image_limit','monthly_audio_limit','monthly_video_limit','additional_character_charge'),
#         }),
#     )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricing_plan', 'start_date', 'end_date', 'is_active')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_developer', 'is_admin', 'is_superuser', 'app_owner_id', 'subscription', 'total_tokens_used')

@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'pricing_plan', 'prompt_tokens_used', 'completion_tokens_used', 'total_tokens_used', 'timestamp')

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('text', 'positive', 'analyzed_at')

@admin.register(EmotionAnalysis)
class EmotionAnalysisAdmin(admin.ModelAdmin):
    list_display = ('text', 'anger_score', 'disgust_score', 'fear_score', 'joy_score', 'neutral_score', 'sadness_score', 'surprise_score', 'analyzed_at')
