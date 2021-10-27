from django.contrib import admin

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'date_added')
    search_fields = ('author',)
    list_filter = ('date_added',)
    empty_value_display = '-empty-'


admin.site.register(Image, ImageAdmin)
