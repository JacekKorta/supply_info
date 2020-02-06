from django.conf import settings
from django.db import models

from serial_numbers.models import Machine


class Issues(models.Model):
    WHERE_IS_THE_PART_CHOICES = []
    FACTORY_STATUS_CHOICES = []
    id = models.IntegerField(max_length=5, unique=True)
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    customer = models.CharField(max_length=52, blank=True, null=True, verbose_name='Klient')
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE, verbose_name='Maszyna')
    part_number = models.CharField(max_length=24, verbose_name='Numer części')
    part_name = models.CharField(max_length=128, verbose_name='Nazwa części')
    quantity = models.CharField(max_length=3, verbose_name='Ilość')
    issue_description = models.TextField(blank=True,
                                         null=True,
                                         verbose_name='Opis usterki')
    where_is_the_part = models.CharField(max_length=15,
                                         choices=WHERE_IS_THE_PART_CHOICES,
                                         default='Czeka na wymianę',
                                         verbose_name='Status wymiany')
    factory_status = models.CharField(max_length=15,
                                      choices=FACTORY_STATUS_CHOICES,
                                      default='Niezgłoszone',
                                      verbose_name='Status u producenta')
    doc_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='Numer proformy')

    def __str__(self):
        return self.id


class Comments(models.Model):
    issue = models.ForeignKey('Issues', on_delete=models.CASCADE, related_name='comments', verbose_name='Komentarz')
    username = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Użytkownik')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True, verbose_name='Widoczny?')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.username, self.issue)



