from datetime import datetime

from django.test import TestCase

from serial_numbers.models import Customer, Machine, ShipmentToCustomer
from serial_numbers.sn_modules import db_save, sn_parser



class SetUpClass(TestCase):
    def setUp(self):
        Machine.objects.create(code='JUNO E1015',
                               serial_number='123456789',
                               delivery_date='2000-01-01')


class SnParserTest(SetUpClass):
    def test_extract_numbers_works(self):
        data = 'A12345678\r\n123456789\r\n987654321\r\n12345678\r\n12345678910\r\n'
        expected_result = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        serials = sn_parser.extract_serial_numbers(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')

    def test_parse_serial_works(self):
        data = ['A12345678', '123456789', '987654321', '12345678', '12345678910', '']
        expected_result = ['123456789', '987654321']
        serials = sn_parser.parse_serials(data)
        self.assertEqual(serials, expected_result, 'The lists are not the same')

    def test_extract_data_to_register_works(self):
        data = 'wrong,A12345678\ngood1,123456789 \ngood2, 987654321\n12345678\nwrong,12345678910\n'
        expected_result = [('good1', '123456789'), ('good2', '987654321')]
        machines = sn_parser.extract_data_to_register_machine(data)
        self.assertEqual(machines, expected_result, 'The list are not the same')


class SnDbSaveTest(TestCase):

    def setUp(self):
        Customer.objects.create(name='Customer1')
        Machine.objects.create(code='Machine1',
                               serial_number='123456789')

    def test_shipment_record(self):
        today = datetime.now()
        delivery_note_number = 'WZ/01/01/2020'
        db_save.shipment_record('Customer1', delivery_note_number, '123456789')
        sample_shipment = ShipmentToCustomer.objects.get(delivery_note_number=delivery_note_number)
        self.assertEqual('WZ/01/01/2020', sample_shipment.delivery_note_number, 'The numbers are not the same!')
        self.assertEqual('Customer1', sample_shipment.customer.name, 'The customers name are not the same!')
        self.assertEqual('Machine1', sample_shipment.item.code, 'The machines name are not the same!')
        self.assertEqual(today.date(), sample_shipment.shipment_date.date(), 'The dates are not the same!')
        self.assertEqual(str(sample_shipment), sample_shipment.delivery_note_number)

    def test_save_delivery(self):
        db_save.save_delivery('123456789', 'Machine1', '2020-01-01')
        db_save.save_delivery('987654321', 'Machine2', '2020-01-01')
        machines = Machine.objects.all()
        self.assertEqual(len(machines), 2)