from django.contrib import admin

from .models import ModuleContent, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'class_name')
    list_filter = ('role',)
    search_fields = ('user__username', 'class_name')


@admin.register(ModuleContent)
class ModuleContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module_type', 'created_at')
    list_filter = ('module_type',)
    search_fields = ('title', 'description')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['image'].label = 'Image / PDF File'
        form.base_fields['image'].help_text = 'Upload image or PDF for this module.'
        return form

# Register your models here.
