from django.contrib import admin

from warranty_parts.models import Comments, Issues
from serial_numbers.models import Machine

class CommentsInlineAdmin(admin.StackedInline):
    model = Comments
    extra = 0


class IssuesAdmin(admin.ModelAdmin):
    def get_machine_serial_number(self, obj):
        machine = Machine.objects.filter(warranty_parts_issue=obj)
        if machine.exists():
            return machine.first().serial_number
        else:
            return None

    def get_machine_code(self, obj):
        machine = Machine.objects.filter(warranty_parts_issue=obj)
        if machine.exists():
            return machine.first().code
        else:
            return None

    def get_comments_sum(self, obj):
        comments = Comments.objects.filter(issue=obj)
        if comments.exists():
            return len(comments)
        else:
            return 'Brak'

    get_machine_serial_number.short_description = 'Numer seryjny'
    get_machine_serial_number.ordering = 'serial_number'
    get_machine_code.short_description = 'Model maszyny'
    get_machine_code.ordering = 'code'
    get_comments_sum.short_description = 'Komentarze'
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
                           'doc_number']}),
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
                    )
    raw_id_fields = ('machine',)

    search_fields = ['id',
                     'time_stamp',
                     'customer',
                     'machine',
                     'part_number',
                     'part_name',
                     'where_is_the_part',
                     'factory_status',
                     'doc_number']
    list_filter = ['time_stamp',
                   'where_is_the_part',
                   'factory_status',
                   'doc_number',
                   ]

    inlines = [CommentsInlineAdmin]



admin.site.register(Comments)
admin.site.register(Issues, IssuesAdmin)
