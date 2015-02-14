from django.contrib import admin

from gallery.models import Banner, BannerImage


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1


class BannerAdmin(admin.ModelAdmin):
    inlines = (BannerImageInline,)
    model = Banner


admin.site.register(Banner, BannerAdmin)
