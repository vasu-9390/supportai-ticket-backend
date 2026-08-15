from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status', 'workload', 'total_assigned', 'total_resolved', 'customer_rating')
    list_filter = ('status', 'role')
    search_fields = ('user__name', 'user__email', 'role')
