from django.urls import path
from .views import (
    AnalyzeTicketView,
    SuggestResponseView,
    AssignAgentView,
    CheckDuplicateView,
    AIInsightsView
)

urlpatterns = [
    path('ai/analyze-ticket/', AnalyzeTicketView.as_view(), name='ai-analyze-ticket'),
    path('ai/suggest-response/', SuggestResponseView.as_view(), name='ai-suggest-response'),
    path('ai/assign-agent/', AssignAgentView.as_view(), name='ai-assign-agent'),
    path('ai/check-duplicate/', CheckDuplicateView.as_view(), name='ai-check-duplicate'),
    path('ai/insights/', AIInsightsView.as_view(), name='ai-insights'),
]
