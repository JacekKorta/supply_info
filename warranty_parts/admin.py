import csv
import io
from datetime import datetime

from django.contrib import admin
from django.http import FileResponse, HttpResponse
from django.utils.html import format_html
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from warranty_parts.models import Comments, Issues
from serial_numbers.models import Machine


class CommentsInlineAdmin(admin.StackedInline):

    def detail_info(self, obj):
        created_date = obj.created.strftime('%Y-%m-%d - %H:%M:%S')
        updated_date = obj.updated.strftime('%Y-%m-%d - %H:%M:%S')

        return format_html(
            '<p>Utworzone przez: <b>{}</b> <br> dnia: <b>{}</b>.<br> Ostatnia aktualizacja: <b>{}</b></p>',
            obj.username,
            created_date,
            updated_date,
        )

    def has_add_permission(self, request, obj=None):
        return False

    model = Comments
    readonly_fields = ['detail_info', 'body']
    fields = ['detail_info', 'body']
    extra = 0
    can_delete = False
    show_change_link = True


class IssuesAdmin(admin.ModelAdmin):
    def get_machine_serial_number(self, obj):
        machine = Machine.objects.filter(warranty_parts_issue=obj).first()
        if machine:
            return machine.serial_number
        else:
            return None

    def get_machine_code(self, obj):
        machine = Machine.objects.filter(warranty_parts_issue=obj).first()
        if machine:
            return machine.code
        else:
            return None

    def get_comments_sum(self, obj):
        comments = Comments.objects.filter(issue=obj)
        if comments.exists():
            return comments.count()
        else:
            return 'Brak'

    def get_add_comment_link(self, obj):
        url = reverse('warranty_parts:add_comment', kwargs={'issue_id': obj})
        return format_html(
            '<a href="{}">Dodaj komentarz</a>', url, obj)

    def change_factory_status_to_reported(self, request, queryset):
        queryset.update(factory_status='zgloszone')

    def change_request_status(self, request, queryset):
        queryset.update(request=True)

    def create_csv_report(self, request, queryset):
        today = datetime.now()
        file_name = f'Warranty_parts_{today.strftime("%Y_%m_%d")}.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['ID',
                         'Machine model',
                         'Serial number',
                         'Part number',
                         'Qty',
                         'Part name',
                         'Issue description',
                         'Reply',
                         'Request'])
        for issue in queryset:
            try:
                writer.writerow([issue.id,
                                 issue.machine.code,
                                 issue.machine.serial_number,
                                 issue.part_number,
                                 issue.quantity,
                                 issue.part_name,
                                 issue.eng_issue_description])
            except AttributeError:
                # for issue separated from machine, ex individual parts or accessories
                writer.writerow([issue.id,
                                 issue.part_number,
                                 '',
                                 '',
                                 issue.quantity,
                                 issue.part_name,
                                 issue.eng_issue_description])
        return response

    def issue_to_pdf(self, request, queryset):
        for issue in queryset:
            buffer = io.BytesIO()
            pdfmetrics.registerFont(TTFont('Arial', '/usr/local/share/fonts/webfonts/arialbi.ttf'))
            page = canvas.Canvas(buffer)
            page.setLineWidth(.3)
            page.setFont("Arial", 8)
            page.drawString(30, 760, f'Zgłoszenie nr: {issue.id}')
            page.drawString(30, 745, f'Numer części: {issue.part_number}')
            page.drawString(30, 730, f'Nazwa części: {issue.part_name}')
            if issue.machine:
                page.drawString(30, 715, f'Model maszyny: {issue.machine.code}')
                page.drawString(30, 700, f'Numer seryjny maszyny: {issue.machine.serial_number}')
            page.drawString(30, 685, f'opsi usterki: {issue.issue_description}')
            page.drawString(30, 670, f'Część została wpisana na proformę: {issue.doc_number}')
            page.line(30, 650, 520, 650)
            page.showPage()
            page.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='raport.pdf')

    create_csv_report.short_description = 'Pobierz raport'
    issue_to_pdf.short_description = 'Pobierz kartę zgłoszenia'
    change_factory_status_to_reported.short_description = 'Oznacz jako: Zgłoszone'
    change_request_status.short_description = 'Oznacz jako: Do zwrotu'
    get_machine_serial_number.short_description = 'Numer seryjny'
    get_machine_serial_number.ordering = 'serial_number'
    get_machine_code.short_description = 'Model maszyny'
    get_machine_code.admin_order_field = 'machine__code'
    get_comments_sum.short_description = 'Komentarze'
    get_add_comment_link.short_description = 'Dodaj komentarz'

    actions = [change_factory_status_to_reported, change_request_status, create_csv_report, issue_to_pdf]
    readonly_fields = ('id', 'time_stamp')
    fieldsets = [
        (None, {'fields': ['id',
                           'time_stamp',
                           'customer',
                           'machine',
                           'part_number',
                           'part_name',
                           'where_is_the_part',
                           'factory_status',
                           'doc_number',
                           'request',
                           'issue_description',
                           'eng_issue_description',
                           ]}),
        ]
    list_display = ('id',
                    'customer',
                    'time_stamp',
                    'get_machine_serial_number',
                    'get_machine_code',
                    'part_number',
                    'part_name',
                    'where_is_the_part',
                    'factory_status',
                    'doc_number',
                    'get_comments_sum',
                    'get_add_comment_link',
                    'request',
                    )
    raw_id_fields = ('machine',)

    search_fields = ['id',
                     'time_stamp',
                     'customer',
                     'machine__code',
                     'machine__serial_number',
                     'part_number',
                     'part_name',
                     'where_is_the_part',
                     'factory_status',
                     'doc_number',
                     ]
    list_filter = ['time_stamp',
                   'where_is_the_part',
                   'factory_status',
                   'doc_number',
                   'request',
                   ]

    inlines = [CommentsInlineAdmin]


class CommentAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if obj is not None and (request.user.is_superuser or (request.user == obj.username)):
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None and (request.user.is_superuser or (request.user == obj.username)):
            return True
        else:
            return False

    def has_add_permission(self, request):
        return False

    def get_changeform_initial_data(self, request, obj=None):
        if obj is not None:
            return {'issue': obj.issue,
                    'username': request.user}
        else:
            return {'username': request.user}

    exclude = ('issue', 'username',)
    readonly_fields = ['issue', 'username', 'updated', 'created']

    fieldsets = [
        (None,{'fields':[
            'issue', 'username', 'created', 'updated','body'
        ]})
    ]


admin.site.register(Comments, CommentAdmin)
admin.site.register(Issues, IssuesAdmin)
