from django.contrib import admin
from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer', 'check_type', 'status')
    list_filter = ('printer', 'check_type', 'status')
# Register your models here.
