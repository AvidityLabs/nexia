from django.contrib import admin
from .models import (
    AIModel,
    User,
    TokenUsage
)

# Register your models here.
admin.site.register(User)
admin.site.register(AIModel)    
admin.site.register(TokenUsage)