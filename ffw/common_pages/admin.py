from django.contrib import admin
from common_pages.models import StaticPage, StaticPageImage


class StaticPageImageInline(admin.TabularInline):
    model = StaticPageImage
    extra = 1

    
class StaticPageAdmin(admin.ModelAdmin):
    inlines = (StaticPageImageInline,)
    model = StaticPage
    list_display = ('title', 'is_active', 'created')
    ordering = ('-created',)
    list_filter = ('is_active',)
    prepopulated_fields = {"slug" : ("title",)}

admin.site.register(StaticPage, StaticPageAdmin)
