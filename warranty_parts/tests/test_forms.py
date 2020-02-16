from datetime import datetime

from django.test import TestCase

from warranty_parts.forms import AddCommentForm, AddIssueForm


class AddCommentFormTest(TestCase):
    # valid form data
    def test_add_new_comment_works(self):
        form = AddCommentForm(data={'body': 'A comment body',
                                    'inform_all': True})
        self.assertTrue(form.is_valid())

    # invalid form data
    def test_add_new_comment_error(self):
        form = AddCommentForm(data={'body': '',
                                    'inform_all': True})
        self.assertFalse(form.is_valid())


class AddIssueFormTest(TestCase):
    # valid form data
    def test_add_issue_form(self):
        today = datetime.now()
        form = AddIssueForm(data={'today': today,
                                  'customer': 'Customer_01',
                                  'machine_serial_number': '1234567898',
                                  'part_number': '000-000-001',
                                  'part_name': 'Part name',
                                  'quantity': 2,
                                  'issue_description': 'Some description',
                                  'document_number': '20-FP/0001'})
        self.assertTrue(form.is_valid())
