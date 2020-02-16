from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase


from public_python.config import EmailConfigData
from warranty_parts.models import Comments, Issues, Machine
from warranty_parts.wp_modules import wp_emails


class TestingWPEmailsNotifications(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', email='adam@example.com', password='adampassword', is_staff=False)
        self.client.login(username='adam', password='adampassword')
        self.machine = Machine.objects.create(code='Machine_01',
                                              serial_number='123456789')
        self.issue = Issues.objects.create(customer='Customer_01',
                                           machine=Machine.objects.get(serial_number='123456789'),
                                           part_number='00000001',
                                           issue_description='sample description',
                                           part_name='Part_01_name',
                                           doc_number='20-FP/0001')
        self.comment = Comments.objects.create(issue=Issues.objects.get(id=self.issue.id),
                                               username=User.objects.get(username=self.user.username),
                                               body='Sample comment')

    def test_wp_emails_send_new_issue_notification(self):
        wp_emails.send_new_issue_notification(self.issue, self.machine)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'[SERWIS] Nowe Zgłosznie nr {self.issue.id}')
        self.assertEqual(mail.outbox[0].body, f'Zgłosznie nr: {self.issue.id}\n'
                                              f'Kod produktu: {self.issue.part_number}\n' 
                                              f'Nazwa produktu: {self.issue.part_name}\n' 
                                              f'Maszyna: {self.machine.code}\n'
                                              f'Nr seryjny: {self.machine.serial_number}\n' 
                                              f'Opis usterki: {self.issue.issue_description}\n'
                                              f'Część została wpisana na: {self.issue.doc_number}\n')
        self.assertEqual(mail.outbox[0].from_email, EmailConfigData.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, EmailConfigData.SERVICE_RECIPIENTS)

    def test_wp_emails_send_new_comment_notification(self):
        wp_emails.send_new_comment_notification(self.issue.id, self.comment)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'[SERWIS][KOMENTARZ] do zgłoszenia {self.issue.id}')
        self.assertEqual(mail.outbox[0].body,
                         f'Użytkownik: {self.comment.username} dodał komentarz do zgłoszenia: {self.issue.id}:\n'
                         f'{self.comment.body}\n')
        self.assertEqual(mail.outbox[0].from_email, EmailConfigData.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, EmailConfigData.SERVICE_RECIPIENTS)