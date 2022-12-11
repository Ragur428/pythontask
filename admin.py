from django.contrib import admin
from .models import *
from .models import AddLessons


class ShopOrderAdmin(admin.ModelAdmin):
    list_filter = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'created_at', 'updated_at']


admin.site.register(AddLessons)
