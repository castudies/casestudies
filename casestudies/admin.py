from django.contrib import admin
from .models import CaseStudy, Notification

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'domain', 'created_at')
    list_filter = ('difficulty', 'domain',)
    search_fields = ('title', 'author', 'case_background', 'domain', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'author_url', 'slug', 'thumbnail')
        }),
        ('Case Details', {
            'fields': ('difficulty', 'domain', 'tags', 'case_background', 'data_summary', 'dataset', 'task')
        }),
        ('Expert Solution', {
            'classes': ('collapse',),
            'fields': ('expert_solution',),
            'description': 'Use the rich text editor below to create formatted expert solutions with images, tables, code snippets, and more.'
        }),
    )

    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }


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