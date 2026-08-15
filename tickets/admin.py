from django.contrib import admin
from .models import Ticket, TicketAttachment, TicketComment

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0

class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'subject', 'customer', 'category', 'priority', 'status', 'assigned_agent', 'created_at')
    list_filter = ('status', 'priority', 'category', 'sentiment')
    search_fields = ('ticket_number', 'subject', 'customer__name', 'customer__email')
    ordering = ('-created_at',)
    inlines = [TicketCommentInline, TicketAttachmentInline]

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    search_fields = ('message', 'ticket__ticket_number', 'user__name')

@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'file_name', 'uploaded_at')
