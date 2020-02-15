from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from warranty_parts.models import Comments, Issues
from serial_numbers.models import Machine


class WarrantyPartsIssuesTest(TestCase):
    def setUp(self):
        Machine.objects.create(code='Machine_01',
                               serial_number='123456789')

    def create_issue(self, customer, serial_number, part_number, part_name, issue_description, doc_number):
        current_datetime = datetime.utcnow()
        return Issues.objects.create(customer=customer,
                                     machine=Machine.objects.get(serial_number=serial_number),
                                     part_number=part_number,
                                     part_name=part_name,
                                     issue_description=issue_description,
                                     doc_number=doc_number,), current_datetime

    def test_correct_issue_creation(self):
        sample_issue, current_datetime = self.create_issue(customer='Customer_01',
                                                           serial_number='123456789',
                                                           part_number='00000001',
                                                           issue_description='sample description',
                                                           part_name='Part_01_name',
                                                           doc_number='20-FP/0001')
        self.assertTrue(isinstance(sample_issue, Issues))
        self.assertTrue(isinstance(sample_issue.machine, Machine),
                        'The machine in issue is not an Machine class instance')
        self.assertEqual(current_datetime.strftime('%Y-%m-%d - %H:%M'),
                         sample_issue.time_stamp.strftime('%Y-%m-%d - %H:%M'))
        self.assertEqual('Customer_01', sample_issue.customer,'The customer codes are not the same')
        self.assertEqual('Machine_01', sample_issue.machine.code, 'Should be Machine_01')
        self.assertEqual('123456789', sample_issue.machine.serial_number, 'The serials numbers are not correct')
        self.assertEqual('00000001', sample_issue.part_number, 'The parts numbers are not the same')
        self.assertEqual('Part_01_name', sample_issue.part_name, 'The parts names are not the same')
        self.assertEqual('sample description', sample_issue.issue_description,
                         'The issues descriptions are not the same')
        self.assertEqual('czeka_na_wymiane', sample_issue.where_is_the_part, '"Where is the part" status is not correct')
        self.assertEqual('niezgloszone', sample_issue.factory_status, '"Factory status" is not correct')
        self.assertEqual(1, sample_issue.quantity, 'Quantity is ont the same')
        self.assertEqual('20-FP/0001', sample_issue.doc_number, 'The documents number are not the same')
        self.assertEqual(None, sample_issue.request, 'The request status are not the same')
        self.assertEqual(str(sample_issue), str(sample_issue.id))


class WarrantyPartsCommentsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')
        Machine.objects.create(code='Machine_01',
                               serial_number='123456789')
        Issues.objects.create(customer='Customer_01',
                                       machine=Machine.objects.get(serial_number='123456789'),
                                       part_number='00000001',
                                       issue_description='sample description',
                                       part_name='Part_01_name',
                                       doc_number='20-FP/0001')

    def create_comment(self, user, issues_id, body):
        current_datetime = datetime.utcnow()
        return Comments.objects.create(issue=Issues.objects.get(id=issues_id),
                                       username=User.objects.get(username=user.username),
                                       body=body), current_datetime

    def test_correct_comment_creation(self):
        sample_comment, current_datetime = self.create_comment(user=self.user,
                                                               issues_id=1,
                                                               body='Sample comment body')
        self.assertTrue(isinstance(sample_comment, Comments))
        self.assertTrue(isinstance(sample_comment.username, User))
        self.assertTrue(isinstance(sample_comment.issue, Issues))
        self.assertEqual('Sample comment body', sample_comment.body)
        self.assertEqual(current_datetime.strftime('%Y-%m-%d - %H:%M'),
                         sample_comment.created.strftime('%Y-%m-%d - %H:%M'))
        self.assertEqual(str(sample_comment), 'Comment by adam on 1')

