from django.urls import path
from .views import (
    AnalyticsDashboardView,
    AnalyticsTicketsView,
    AnalyticsAgentsView,
    AnalyticsAIView
)

urlpatterns = [
    path('analytics/dashboard/', AnalyticsDashboardView.as_view(), name='analytics-dashboard'),
    path('analytics/tickets/', AnalyticsTicketsView.as_view(), name='analytics-tickets'),
    path('analytics/agents/', AnalyticsAgentsView.as_view(), name='analytics-agents'),
    path('analytics/ai/', AnalyticsAIView.as_view(), name='analytics-ai'),
]
