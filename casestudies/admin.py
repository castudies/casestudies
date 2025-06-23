from django.contrib import admin
from .models import CaseStudy

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
        }),
    )
