from django.conf import settings
from django.db import models

from serial_numbers.models import Machine


class Issues(models.Model):
    WHERE_IS_THE_PART_CHOICES = [
        ('czeka_na_wymiane', 'Czeka na wymianę'),
        ('odrzucone', 'Odrzucone'),
        ('wydana_z_maszyny', 'Wydana z maszyny'),
        ('wymieniona','Wymieniona'),
    ]
    FACTORY_STATUS_CHOICES = [
        ('czeka_na_wymiane', 'Czeka na wymianę'),
        ('niezgloszone', 'Niezgłoszone'),
        ('odrzucone', 'Odrzucone'),
        ('wymienione', 'Wymienione'),
        ('zgloszone', 'Zgłoszone'),
    ]
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    customer = models.CharField(max_length=52, blank=True, null=True, verbose_name='Klient')
    machine = models.ForeignKey(Machine,
                                   to_field='serial_number',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   verbose_name='Maszyna',
                                   related_name='warranty_parts_issue')
    part_number = models.CharField(max_length=24, verbose_name='Numer części')
    part_name = models.CharField(max_length=128, verbose_name='Nazwa części')
    quantity = models.IntegerField(default=1, verbose_name='Ilość')
    issue_description = models.TextField(blank=True,
                                         null=True,
                                         verbose_name='Opis usterki')
    where_is_the_part = models.CharField(max_length=20,
                                         choices=WHERE_IS_THE_PART_CHOICES,
                                         default='czeka_na_wymiane',
                                         verbose_name='Status wymiany')
    factory_status = models.CharField(max_length=20,
                                      choices=FACTORY_STATUS_CHOICES,
                                      default='niezgloszone',
                                      verbose_name='Status u producenta')
    doc_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='Proforma')
    request = models.BooleanField(default=None, null=True, verbose_name='Do zwrotu')

    class Meta:
        verbose_name = 'Zgłoszenie'
        verbose_name_plural = 'Zgłoszenia'

    def __str__(self):
        return str(self.id)


class Comments(models.Model):
    issue = models.ForeignKey('Issues', on_delete=models.CASCADE, related_name='comments', verbose_name='Komentarz')
    username = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Użytkownik', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.username, self.issue)



