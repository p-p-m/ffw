from django.contrib import admin

from gallery.models import Banner, BannerImage, GalleryPrimImage, GalleryImage


class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1


class BannerAdmin(admin.ModelAdmin):
    inlines = (BannerImageInline,)
    model = Banner


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


class GalleryPrimImageAdmin(admin.ModelAdmin):
    inlines = (GalleryImageInline,)
    model = GalleryPrimImage


admin.site.register(GalleryPrimImage, GalleryPrimImageAdmin)
admin.site.register(Banner, BannerAdmin)
