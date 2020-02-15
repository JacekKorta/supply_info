from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from serial_numbers.models import Machine
from warranty_parts.models import Issues


class UserLoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', email='adam@example.com', password='adampassword', is_staff=False)
        self.client.login(username='adam', password='adampassword')


class StaffUserLoggedInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', email='adam@example.com', password='adampassword', is_staff=True)
        self.client.login(username='adam', password='adampassword')
        Machine.objects.create(code='Machine_01',
                               serial_number='123456789')
        Issues.objects.create(customer='Customer_01',
                              machine=Machine.objects.get(serial_number='123456789'),
                              part_number='00000001',
                              issue_description='sample description',
                              part_name='Part_01_name',
                              doc_number='20-FP/0001')


class TestSiteStaffUserLogged(StaffUserLoggedInTestCase):
    def test_add_issue_page_works(self):
        today = datetime.now()
        response = self.client.get(reverse('warranty_parts:add_issue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warranty_parts/add_issue.html')
        self.assertTemplateUsed(response, 'supply_info/base.html')
        self.assertContains(response, 'Nowe zgłoszenie')
        self.assertContains(response, 'Nazwa klienta:')
        self.assertContains(response, 'Numer seryjny maszyny:')
        self.assertContains(response, 'Numer cześci:')
        self.assertContains(response, 'Nazwa części:')
        self.assertContains(response, 'Ilość')
        self.assertContains(response, '1')
        self.assertContains(response, 'Opis usterki:')
        self.assertContains(response, 'Numer proformy:')
        self.assertContains(response, f'{today.strftime("%y")}-FP/')
        self.assertContains(response, 'Zapisz')


    def test_add_comment_page_works(self):
        response = self.client.get(reverse('warranty_parts:add_comment', kwargs={'issue_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'warranty_parts/add_comment.html')
        self.assertTemplateUsed(response, 'supply_info/base.html')
        self.assertContains(response, 'Dodaj komentarz')
        self.assertContains(response, '1')
        self.assertContains(response, 'adam')
        self.assertContains(response, 'Komentarz:')
        self.assertContains(response, 'Powiadom innych:')
        self.assertContains(response, 'Zapisz')



class TestSiteUserLogged(UserLoggedInTestCase):
    def test_add_issue_page_works(self):
        response = self.client.get(reverse('warranty_parts:add_issue'))
        self.assertEqual(response.status_code, 302)

    def test_add_comment_page_works(self):
        response = self.client.get(reverse('warranty_parts:add_comment', kwargs={'issue_id': 1}))
        self.assertEqual(response.status_code, 302)


class TestSiteAnonymus(TestCase):
    def test_add_issue_page_works(self):
        response = self.client.get(reverse('warranty_parts:add_issue'))
        self.assertEqual(response.status_code, 302)

    def test_add_comment_page_works(self):
        response = self.client.get(reverse('warranty_parts:add_comment', kwargs={'issue_id': 1}))
        self.assertEqual(response.status_code, 302)