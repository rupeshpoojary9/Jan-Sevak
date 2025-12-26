from django.contrib import admin
from .models import Complaint, Category, Ward, Verification, UserProfile

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'ward', 'status', 'urgency_score', 'created_at')
    list_filter = ('status', 'category', 'ward', 'urgency_score')
    search_fields = ('title', 'description', 'location_address')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='RESOLVED')
        self.message_user(request, f"{updated} complaints marked as RESOLVED.")
    mark_as_resolved.short_description = "Mark selected complaints as Resolved"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'full_name', 'officer_email')
    search_fields = ('name', 'full_name', 'officer_email')

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'complaint', 'user', 'verified_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'badges')
