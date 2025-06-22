from django.contrib import admin
from .models import CaseStudy

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'domain', 'created_at')
    list_filter = ('difficulty', 'domain',)
    search_fields = ('title', 'author', 'case_background', 'domain')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'slug', 'thumbnail')
        }),
        ('Case Details', {
            'fields': ('difficulty', 'domain', 'case_background', 'data_summary', 'dataset', 'task')
        }),
        ('Expert Solution', {
            'classes': ('collapse',),
            'fields': ('expert_solution',),
        }),
    )
