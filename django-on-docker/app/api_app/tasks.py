from django.conf import settings as conf_settings

from .models import Check

from celery import shared_task
from fpdf import FPDF


@shared_task()
def generate_pdf_task():
    checks = Check.objects.filter(status=Check.NEW)

    if not checks.exists():
        print('Nothing to do, checks is not exists')
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    line_height = 5

    data = ['Name', 'price', 'total']
    col_num = 0
    for element in data:

        col_width = 75 if col_num == 0 else 56

        pdf.set_fill_color(r=64)
        pdf.set_text_color(r=255)

        pdf.cell(w=col_width, h=line_height, txt=element, border=1, fill=True, align='C')
        col_num += 1

    pdf.ln(line_height)

    for check in checks:
        col_num = 0

        pdf.set_fill_color(r=255)
        pdf.set_text_color(r=0)

        for item in check.order['fields']['order']['items']:
            col_width = 75
            pdf.cell(w=col_width, h=line_height, txt=item['name'], border=1, fill=True, align='C')
            col_num += 1

            col_width = 56
            pdf.cell(w=col_width, h=line_height, txt=str(item['price']) + '$', border=1, fill=True, align='C')
            col_num += 1
            break
        col_width = 56
        total = check.order['fields']['order']['total']
        pdf.cell(w=col_width, h=line_height, txt=str(total) + '$', border=1, fill=True, align='C')

        filename = f"/pdfs/check_{check.order['fields']['order']['id']}_{check.check_type}.pdf"

        pdf.output(f"{conf_settings.MEDIA_ROOT}{filename}")
        check.pdf_file = filename
        check.status = Check.PRINTED
        check.save()
    print('------   Ready   ------')


def generate_pdf():
    checks = Check.objects.filter(status=Check.NEW)

    if not checks.exists():
        print('Nothing to do, checks is not exists')
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    line_height = 5

    data = ['Name', 'price', 'total']
    col_num = 0
    for element in data:

        col_width = 75 if col_num == 0 else 56

        pdf.set_fill_color(r=64)
        pdf.set_text_color(r=255)

        pdf.cell(w=col_width, h=line_height, txt=element, border=1, fill=True, align='C')
        col_num += 1

    pdf.ln(line_height)

    for check in checks:
        col_num = 0

        pdf.set_fill_color(r=255)
        pdf.set_text_color(r=0)

        for item in check.order['fields']['order']['items']:
            col_width = 75
            pdf.cell(w=col_width, h=line_height, txt=item['name'], border=1, fill=True, align='C')
            col_num += 1

            col_width = 56
            pdf.cell(w=col_width, h=line_height, txt=str(item['price']) + '$', border=1, fill=True, align='C')
            col_num += 1
            break
        col_width = 56
        total = check.order['fields']['order']['total']
        pdf.cell(w=col_width, h=line_height, txt=str(total) + '$', border=1, fill=True, align='C')

        filename = f"/pdfs/check_{check.order['fields']['order']['id']}_{check.check_type}.pdf"

        pdf.output(f"{conf_settings.MEDIA_ROOT}{filename}")
        check.pdf_file = filename
        check.status = Check.PRINTED
        check.save()
        print('------   Ready   ------')