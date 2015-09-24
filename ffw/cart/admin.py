from django.contrib import admin

from . import models


class OrderedProductInline(admin.TabularInline):
    model = models.OrderedProduct
    fields = ('name', 'code', 'price', 'quant', 'total')
    readonly_fields = fields
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderedProductInline, )
    model = models.Order
    list_display = ('id', 'name', 'email', 'phone', 'is_resolved', 'count', 'total')
    list_filter = ('is_resolved',)
    ordering = ('-created',)


admin.site.register(models.Order, OrderAdmin)
