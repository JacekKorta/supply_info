from smtplib import SMTPException

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import loader
from django.shortcuts import get_object_or_404

from supply_info.models import Alert, Product
from public_python.config import EmailConfigData


class Command(BaseCommand):
    help = 'responsible for sending notifications for alerts'

    @staticmethod
    def get_users_pk():
        return Alert.objects.order_by().values_list('user', flat=True).distinct()

    @staticmethod
    def get_user_alerts(user_pk):
        return Alert.objects.filter(user_id=user_pk).filter(is_active=True)

    @staticmethod
    def alerts_to_send(alerts):
        alerts_to_send = []
        for alert in alerts:
            product = get_object_or_404(Product, pk=alert.product.id)
            if alert.less_or_equal:
                if alert.qty_alert_lvl >= product.get_prod_availability:
                    alerts_to_send.append((alert, product.get_prod_availability))
            else:
                if alert.qty_alert_lvl < product.get_prod_availability:
                    alerts_to_send.append((alert, product.get_prod_availability))
        return alerts_to_send


    @staticmethod
    def send_alert_email(alerts_to_send, email_to):
        html_message = loader.render_to_string('supply_info/emails/alert_list_email.html',
                                               {'alerts_to_send': alerts_to_send})
        subject = 'JANOME - Alerty o dostępności produktów'
        from_email = 'Janome - powiadomienia automatyczne <powiadomienia@janomeklub.pl>'
        to = [email_to]
        send_mail(subject=subject,
                  from_email=from_email,
                  recipient_list=to,
                  message='',
                  fail_silently=False,
                  html_message=html_message)

    @staticmethod
    def send_alert_recap(alerts_list):
        html_message = loader.render_to_string('supply_info/emails/alerts_recap.html',
                                               {'alerts_list': alerts_list})
        subject = f'[JANOMEKLUB] - Zestawienie wysłanych alertów'
        from_email = 'Janome - powiadomienia automatyczne <powiadomienia@janomeklub.pl>'
        to = EmailConfigData.OFFICE_RECIPIENTS
        send_mail(subject=subject,
                  from_email=from_email,
                  recipient_list=to,
                  message='',
                  fail_silently=False,
                  html_message=html_message)

    def handle(self, **options):
        users_pk = self.get_users_pk()
        alerts_list = []
        for pk in users_pk:
            user_email = get_object_or_404(User, pk=pk).email
            user_alerts = self.get_user_alerts(pk)
            alerts_to_send = self.alerts_to_send(user_alerts)
            if user_email and alerts_to_send:
                try:
                    self.send_alert_email(alerts_to_send, user_email)
                    alerts_list.append((alerts_to_send, user_email))
                    print(f'wyslano alerty do {user_email}')
                except SMTPException as e:
                    print(f'Error code {e.smtp_code} - {e.smtp_error}')
                except Exception as e:
                    print(f'Błąd przy wysyalaniu maili: {e}')
                try:
                    for alert, _ in alerts_to_send:
                        alert.is_active = False
                        alert.save()
                except Exception as e:
                    print(f'bład podczas zmiany stanu: {e}')

            if not user_email and alerts_to_send:
                print(pk)
                print('Brak adresu email')

        self.send_alert_recap(alerts_list)

