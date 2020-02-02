from django.test import TestCase

from serial_numbers.forms import ShipmentForm
from serial_numbers.models import Customer, Machine


class SetUpClass(TestCase):
    def setUp(self):
        Machine.objects.create(code='JUNO E1015',
                               serial_number='123456789',
                               delivery_date='2000-01-01')

        Customer.objects.create(name='ExampleCustomer',
                                tax_number='0123456789',
                                email='example@domain.com')


class ShipmentToCustomerTest(SetUpClass):
    def test_shipment_form(self):
        customer = Customer.objects.get(name='ExampleCustomer')
        form = ShipmentForm(data={'customer': customer.id,
                                  'delivery_note_number':'00/00',
                                  'shipment':'A12345678\n123456789\n987654321\n12345678\n12345678910\n'})
        self.assertTrue(form.is_valid())
