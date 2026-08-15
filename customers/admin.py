from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'tier', 'created_at')
    list_filter = ('tier', 'company')
    search_fields = ('name', 'email', 'company')
    ordering = ('-created_at',)
