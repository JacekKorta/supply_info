import csv
from datetime import datetime

from django.http import FileResponse, HttpResponse


class AdminAddons:

    def create_csv_report_serial_numbers(self, request, queryset):
        today = datetime.now()
        file_name = f'Serial_numbers_{today.strftime("%Y_%m_%d")}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['WZ',
                         'Klient',
                         'Maszyna',
                         'Numer seryjny',
                         'Data skanowania',
                         ])
        for delivery_note in queryset:
            writer.writerow([delivery_note.delivery_note_number,
                             delivery_note.customer,
                             delivery_note.item,
                             delivery_note.item.serial_number,
                             delivery_note.shipment_date,
                             ])
        return response

