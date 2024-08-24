from django.contrib import admin
from .models import Day

print("Admin.py is being loaded")


class DayAdmin(admin.ModelAdmin):
    list_display = ['name']  # This will display the 'name' field in the admin list view


admin.site.register(Day, DayAdmin)
