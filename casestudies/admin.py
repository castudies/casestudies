from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CaseStudy, UserSubmittedCaseStudy, Notification, UploadLog
from .utils import send_approval_notification_to_user, send_rejection_notification_to_user
from .forms import UserSubmittedCaseStudyAdminForm
from django.utils import timezone

class BaseCaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'domain', 'difficulty', 'created_at')
    list_filter = ('domain', 'difficulty', 'created_at')
    search_fields = ('title', 'author', 'case_background', 'task')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'author_url', 'domain', 'difficulty', 'tags')
        }),
        ('Media', {
            'fields': ('thumbnail', 'dataset'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('case_background', 'data_summary', 'task', 'expert_solution')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show all admin case studies
        return qs
    
    # Custom CSS for the admin interface
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

@admin.register(CaseStudy)
class CaseStudyAdmin(BaseCaseStudyAdmin):
    pass

class BaseUserSubmittedCaseStudyAdmin(admin.ModelAdmin):
    """Admin interface for user-submitted case studies"""
    form = UserSubmittedCaseStudyAdminForm
    list_display = ('title', 'author', 'submitter_email', 'domain', 'difficulty', 'submitted_at', 'status_badge', 'dataset_link', 'thumbnail_preview')
    list_filter = ('is_approved', 'domain', 'difficulty', 'submitted_at')
    search_fields = ('title', 'author', 'submitter_email', 'case_background', 'task')
    readonly_fields = ('submitted_at',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'submitter_email', 'domain', 'difficulty', 'tags')
        }),
        ('Media', {
            'fields': ('thumbnail', 'dataset'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('case_background', 'task', 'expert_solution', 'options')
        }),
        ('Status & Approval', {
            'fields': ('is_approved', 'admin_notes', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_submissions', 'reject_submissions', 'mark_as_pending']
    
    def status_badge(self, obj):
        if obj.is_approved is None:
            return format_html('<span style="background-color: #fbbf24; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Pending</span>')
        elif obj.is_approved:
            return format_html('<span style="background-color: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Approved</span>')
        else:
            return format_html('<span style="background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">Rejected</span>')
    status_badge.short_description = 'Status'
    
    def approve_submissions(self, request, queryset):
        count = 0
        for case_study in queryset:
            if case_study.is_approved is not True:
                case_study.is_approved = True
                case_study.reviewed_at = timezone.now()
                case_study.save()
                if case_study.submitter_email:
                    send_approval_notification_to_user(case_study, request)
                count += 1
        self.message_user(request, f'{count} user submission(s) have been approved.')
    
    approve_submissions.short_description = "Approve selected submissions"
    
    def reject_submissions(self, request, queryset):
        count = 0
        for case_study in queryset:
            if case_study.is_approved is not False:
                case_study.is_approved = False
                case_study.reviewed_at = timezone.now()
                case_study.save()
                if case_study.submitter_email:
                    send_rejection_notification_to_user(case_study, request)
                count += 1
        self.message_user(request, f'{count} user submission(s) have been rejected.')
    
    reject_submissions.short_description = "Reject selected submissions"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(is_approved=None, reviewed_at=None)
        self.message_user(request, f'{updated} user submission(s) have been marked as pending.')
    
    mark_as_pending.short_description = "Mark selected submissions as pending"
    
    def has_add_permission(self, request):
        return False  # Don't allow adding user submissions through admin

    def dataset_link(self, obj):
        if obj.dataset:
            return format_html('<a href="{}" download>{}</a>', obj.dataset.url, obj.dataset_filename)
        return '-'
    dataset_link.short_description = 'Dataset'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-width:120px; max-height:60px; border-radius:6px;" />', obj.thumbnail.url)
        return '-'
    thumbnail_preview.short_description = 'Thumbnail'

    # Custom CSS for the admin interface
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


@admin.register(UserSubmittedCaseStudy)
class UserSubmittedCaseStudyAdmin(BaseUserSubmittedCaseStudyAdmin):
    pass

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "body", "button_text")
    fieldsets = (
        (None, {
            'fields': ("title", "body", "video", "is_active", "delay_seconds")
        }),
        ("Button", {
            'fields': ("button_text", "button_link")
        }),
    )

@admin.register(UploadLog)
class UploadLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'email', 'ip', 'dataset', 'thumbnail')
    search_fields = ('email', 'ip', 'dataset', 'thumbnail')
    list_filter = ('timestamp',)