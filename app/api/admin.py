from django.contrib import admin

from .models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'author', 'date_added', 'views')
    search_fields = ('author',)
    list_filter = ('date_added', 'views')
    empty_value_display = '-empty-'


admin.site.register(Image, ImageAdmin)
