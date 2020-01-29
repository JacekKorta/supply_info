from django.test import TestCase

from ..models import Machine
from ..sn_modules.sn_parser import extract_serial_numbers, parse_serials


class SetUpClass(TestCase):
    def setUp(self):
        Machine.objects.create(code='JUNO E1015',
                               serial_number='123456789',
                               delivery_date='2000-01-01')


class ShipmentToCustomerTest(SetUpClass):
    def test_extract_numbers(self):
        data = 'A12345678\r\n123456789\r\n987654321\r\n12345678\r\n12345678910\r\n'
        expected_result = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        serials = extract_serial_numbers(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')

    def test_parse_serial(self):
        data = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        expected_result = ['123456789', '987654321']
        serials = parse_serials(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')



