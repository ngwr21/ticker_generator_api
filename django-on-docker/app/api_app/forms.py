
from django import forms

from .models import Printer, Check


class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ('name', 'api_key', 'check_type', 'point_id')


class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = ('printer', 'check_type', 'order', 'status')