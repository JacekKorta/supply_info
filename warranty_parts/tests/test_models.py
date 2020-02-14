from datetime import datetime

from django.test import TestCase
from warranty_parts.models import Comments, Issues
from serial_numbers.models import Machine



class WarrantyPartsIssuesTest(TestCase):
    def setUp(self):
        Machine.objects.crete(code='Machine_01',
                              serial_number='123456789')

    def create_issue(self, customer, serial_number, part_number, part_name, issue_description, doc_number):
        current_datetime = datetime.now()
        return Issues.objects.create(customer=customer,
                                     serial_number=serial_number,
                                     part_number=part_number,
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
        self.assertEqual('Customer_01', sample_issue.customer,'The customer codes are not the same')
        self.assertEqual('Machine_01', sample_issue.machine, 'Should be Machine_01')
        self.assertEqual('00000001', sample_issue.part_number, 'The parts numbers are not the same')
        self.assertEqual('sample description', sample_issue.issue_description,
                         'The issues descriptions are not the same')
        self.assertEqual('Czeka na wymianę', sample_issue.where_is_the_part, '"Where is the part" status is not correct')
        self.assertEqual('Czeka na wymianę', sample_issue.factory_status, '"Factory status" is not correct')
        self.assertEqual(1, sample_issue.quantity, 'Quantity is ont the same')
        self.assertEqual('20-FP/0001', sample_issue.doc_number, 'The documents number are not the same')
        self.assertEqual(None, sample_issue.reques, 'The request status are not the same')
