from django.contrib.auth.models import User
from django.test import TestCase

from serial_numbers.models import Machine
from warranty_parts.models import Comments, Issues
from warranty_parts.wp_modules import db_save as wp_dbs


class WPDbSaveSaveIssuesTest(TestCase):
    def setUp(self):
        Machine.objects.create(code='Machine_01',
                               serial_number='123456789')

    def test_save_issue_unregistered_machine(self):
        form_dict = {'customer': 'Customer_01',
                     'machine_sn': '012345678',
                     'part_number': '000-000-001',
                     'part_name': 'Part name01',
                     'quantity': 2,
                     'issue_description': 'Issue 01 description',
                     'document_number': '20-FP/001'}
        expected_issue, returned_machine = wp_dbs.save_issues(form_dict)
        self.assertTrue(isinstance(expected_issue, Issues))
        self.assertFalse(isinstance(returned_machine, Machine))
        self.assertEqual(expected_issue.customer, 'Customer_01')
        self.assertEqual(expected_issue.machine, None, 'This field should be empty')
        self.assertEqual(expected_issue.part_number, '000-000-001')
        self.assertEqual(expected_issue.part_name, 'Part name01')
        self.assertEqual(expected_issue.quantity, 2)
        self.assertEqual(expected_issue.issue_description, 'Issue 01 description')
        self.assertEqual(expected_issue.where_is_the_part, 'czeka_na_wymiane')
        self.assertEqual(expected_issue.factory_status, 'niezgloszone')
        self.assertEqual(expected_issue.doc_number, '20-FP/001')
        self.assertEqual(expected_issue.request, None)

    def test_save_issue_registered_machine(self):
        form_dict = {'customer': 'Customer_01',
                     'machine_sn': '123456789',
                     'part_number': '000-000-001',
                     'part_name': 'Part name01',
                     'quantity': 2,
                     'issue_description': 'Issue 01 description',
                     'document_number': '20-FP/001'}
        expected_issue, returned_machine = wp_dbs.save_issues(form_dict)
        self.assertTrue(isinstance(expected_issue, Issues))
        self.assertTrue(isinstance(returned_machine, Machine))
        self.assertEqual(expected_issue.customer, 'Customer_01')
        self.assertEqual(expected_issue.machine.code, 'Machine_01')
        self.assertEqual(expected_issue.machine.serial_number, '123456789')
        self.assertEqual(expected_issue.part_number, '000-000-001')
        self.assertEqual(expected_issue.part_name, 'Part name01')
        self.assertEqual(expected_issue.quantity, 2)
        self.assertEqual(expected_issue.issue_description, 'Issue 01 description')
        self.assertEqual(expected_issue.where_is_the_part, 'czeka_na_wymiane')
        self.assertEqual(expected_issue.factory_status, 'niezgloszone')
        self.assertEqual(expected_issue.doc_number, '20-FP/001')
        self.assertEqual(expected_issue.request, None)


class WPDbSaveSaveCommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')
        Machine.objects.create(code='Machine_01',
                               serial_number='123456789')
        self.issues = Issues.objects.create(customer='Customer_01',
                                            machine=Machine.objects.get(serial_number='123456789'),
                                            part_number='00000001',
                                            issue_description='sample description',
                                            part_name='Part_01_name',
                                            doc_number='20-FP/0001')

    def test_save_comment(self):
        expected_comment = wp_dbs.save_comment('comment body', self.issues.id, self.user)
        self.assertTrue(isinstance(expected_comment, Comments))
        self.assertTrue(isinstance(expected_comment.issue, Issues))
        self.assertTrue(isinstance(expected_comment.username, User))
        self.assertEqual(expected_comment.body, 'comment body')
        self.assertEqual(expected_comment.username.username, 'adam')
        self.assertEqual(str(expected_comment), f'Comment by adam on {self.issues.id}')