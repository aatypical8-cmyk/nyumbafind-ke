from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'town', 'county', 'price', 'bedrooms', 'is_available', 'landlord']
    list_filter = ['county', 'is_available', 'bedrooms']
    search_fields = ['title', 'town', 'description']
    readonly_fields = ['created_at', 'updated_at']
