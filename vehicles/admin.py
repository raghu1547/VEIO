from django.contrib import admin
from . import models
# Register your models here.


class RegvehAdmin(admin.ModelAdmin):
    list_display = ('vn', 'name', 'post', 'contact')
    list_display_links = ('vn', 'name')


class GesvehAdmin(admin.ModelAdmin):
    list_display = ('vn', 'name', 'contact', 'nod', 'firstentry')
    list_display_links = ('vn', 'name')


class FlowAdmin(admin.ModelAdmin):
    list_display = ('vn', 'timein', 'timeout')
    list_display_links = ('vn', 'timein', 'timeout')


admin.site.register(models.Regveh, RegvehAdmin)
admin.site.register(models.Gesveh, GesvehAdmin)
admin.site.register(models.Flow, FlowAdmin)
