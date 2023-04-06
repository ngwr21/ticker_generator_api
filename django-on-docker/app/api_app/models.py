from django.db import models
from django.db.models import JSONField


class Printer(models.Model):
    KITCHEN = 'kitchen'

    CLIENT = 'client'
    CHECK_TYPES = [
        (KITCHEN, 'Kitchen'),
        (CLIENT, 'Client'),
    ]
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=7, choices=CHECK_TYPES)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name


class Check(models.Model):
    NEW = 'new'
    RENDERED = 'rendered'
    PRINTED = 'printed'
    CHECK_STATUSES = [
        (NEW, 'New'),
        (RENDERED, 'Rendered'),
        (PRINTED, 'Printed'),
    ]

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=7, choices=Printer.CHECK_TYPES)
    order = JSONField()
    status = models.CharField(max_length=8, choices=CHECK_STATUSES, default=NEW)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def __str__(self):
        return f"Check for {self.printer.name} ({self.check_type}) - {self.status}"

    class Meta:
        unique_together = ('printer', 'order')
        verbose_name = 'Check'
        verbose_name_plural = 'Checks'