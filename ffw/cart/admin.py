from django.contrib import admin

from . import models


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    list_display = ('id', 'name', 'email', 'phone',)
    ordering = ('-created',)


admin.site.register(models.Order, OrderAdmin)

