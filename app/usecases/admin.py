from django.contrib import admin
from .models import UseCase, UseCaseCategory

class UseCaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'function_name', 'description', 'navigateTo', 'category']
    list_filter = ['category']
    search_fields = ['title', 'function_name']

admin.site.register(UseCase, UseCaseAdmin)
admin.site.register(UseCaseCategory)
