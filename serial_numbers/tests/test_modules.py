from django.test import TestCase

from serial_numbers.models import Machine
from serial_numbers.sn_modules.sn_parser import extract_data_to_register_machine, extract_serial_numbers, parse_serials


class SetUpClass(TestCase):
    def setUp(self):
        Machine.objects.create(code='JUNO E1015',
                               serial_number='123456789',
                               delivery_date='2000-01-01')


class ShipmentToCustomerTest(SetUpClass):
    def test_extract_numbers_works(self):
        data = 'A12345678\r\n123456789\r\n987654321\r\n12345678\r\n12345678910\r\n'
        expected_result = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        serials = extract_serial_numbers(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')

    def test_parse_serial_works(self):
        data = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        expected_result = ['123456789', '987654321']
        serials = parse_serials(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')

    def test_extract_data_to_register_works(self):
        data = 'wrong,A12345678\ngood1,123456789 \ngood2, 987654321\n12345678\nwrong,12345678910\n'
        expected_result = [('good1', '123456789'), ('good2', '987654321')]
        machines = extract_data_to_register_machine(data)
        self.assertEqual(machines, expected_result, 'The list are not the same')

