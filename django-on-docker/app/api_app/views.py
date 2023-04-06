from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse

from .models import Printer, Check
from .tasks import generate_pdf_task, generate_pdf

import json
import os


@csrf_exempt
def create_check(request, api_key):
    if request.method == 'POST':
        try:
            printer = Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid API key'})

        data = json.loads(request.body)
        check_type = data['fields']['check_type']

        test = Check.objects.filter(order__fields__order__id=data['fields']['order']['id'])
        if test.exists():
            return JsonResponse({'error': 'Check already exists', 'id': test.first().order['fields']['order']['id']})

        check1 = Check(printer=printer, check_type=check_type, order=data)
        check1.save()

        check2_type = Printer.KITCHEN if check_type == Printer.CLIENT else Printer.CLIENT

        check2 = Check(printer=printer, check_type=check2_type, order=data)
        check2.save()

        try:
            generate_pdf_task.delay()
        except:
            generate_pdf()

        return JsonResponse({'success_check1': check1.order,
                             'success_check2': check2.order})
    else:
        printer = request.user.id
        user_checks = Check.objects.filter(printer=printer)
        return JsonResponse({'checks': len(user_checks)})


def list_checks(request, api_key):
    try:
        printer = Printer.objects.get(api_key=api_key)
    except Printer.DoesNotExist:
        return JsonResponse({'error': 'Invalid API key'})

    checks = Check.objects.filter(printer=printer)
    check_list = [{'id': check.id, 'order': check.order} for check in checks]

    return JsonResponse({'checks': check_list})


def download_pdf(request, api_key, check_id):
    try:
        printer = Printer.objects.get(api_key=api_key)
    except Printer.DoesNotExist:
        return JsonResponse({'error': 'Invalid API key'})
    check = get_object_or_404(Check, pk=check_id, printer=printer)

    if check.status != Check.PRINTED:
        return JsonResponse({'error': 'PDF not generated yet'})
    pdf_path = check.pdf_file.path

    if not os.path.exists(pdf_path):
        return JsonResponse({'error': 'PDF file not found'})

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{check_id}.pdf"'

    return response


def view_checks(request, api_key):
    if request.method == 'GET':
        printer = Printer.objects.filter(api_key=api_key)
        if printer.exists():
            printer = printer.first()

        checks = Check.objects.filter(printer=printer, status=Check.NEW)
        context = {'checks': checks}

        return render(request, 'api_app/index.html', context)