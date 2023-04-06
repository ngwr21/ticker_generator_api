from .models import *
from rest_framework import serializers

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    #
    # check_items = CheckItemSerializer(many=True)
    class Meta:
        model = Check
        fields = '__all__'
