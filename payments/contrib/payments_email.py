from django.template import loader

from django.core.mail import send_mail

from serial_numbers.models import Customer
from public_python.config import EmailConfigData


class Email:

    @staticmethod
    def get_customer_email(customer_code):
        try:
            customer = Customer.objects.get(name=customer_code)
            if customer.email:
                return customer.email
            else:
                return 'Ten kontrahent nie ma podanego adresu email.'
        except Customer.DoesNotExist:
            return 'Ten kontrahent nie istnieje w bazie.'

    @staticmethod
    def send_payment_notification(email_to, data, customer_name):
        html_message = loader.render_to_string('payments/emails/delayed_payments_email_notification.html',
                                               {'data': data,
                                                'customer_name': customer_name})
        subject = f'{customer_name} Zaległe płatności dla ETI'
        from_email = 'Janome - Zaległe płatności <powiadomienia@janomeklub.pl>'
        to = [email_to, EmailConfigData.OFFICE_RECIPIENTS[0]]
        try:
            send_mail(subject=subject,
                      from_email=from_email,
                      recipient_list=to,
                      message='',
                      fail_silently=False,
                      html_message=html_message)
            return f'Wysłano wiadomosć do: {customer_name} na adres {email_to}.'
        except Exception as e:
            return f'Error: {e}.'

