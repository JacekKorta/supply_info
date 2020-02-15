from datetime import datetime

from django.test import TestCase

from serial_numbers.models import Customer, Machine, ShipmentToCustomer


class SerialNumberCustomerTest(TestCase):

    def create_customer(self, name, tax_number=None, email=None):
        return Customer.objects.create(name=name,
                                       tax_number=tax_number,
                                       email=email,
                                       )

    def test_correct_customer_creation(self):
        sample_customer = self.create_customer(name='Customer1',
                                               tax_number='pl123-12-51-264',
                                               email='example@domain.com',
                                               )
        self.assertTrue(isinstance(sample_customer, Customer))
        self.assertEqual('Customer1', sample_customer.name, 'The names are not the same')
        self.assertEqual('pl123-12-51-264', sample_customer.tax_number, 'The tax numbers are not the same')
        self.assertEqual('example@domain.com', sample_customer.email, 'The emails addresses are not the same')
        self.assertEqual(str(sample_customer), sample_customer.name)

    def test_simple_sample_customer(self):
        sample_customer = self.create_customer(name='Customer1')
        self.assertTrue(isinstance(sample_customer, Customer))
        self.assertEqual('Customer1', sample_customer.name, 'The names are not the same')


class SerialNumberMachineTest(TestCase):

    def create_machine(self, code, serial_number, delivery_date=None):
        return Machine.objects.create(code=code,
                                      serial_number=serial_number,
                                      delivery_date=delivery_date)

    def test_correct_machine_creation(self):
        sample_machine = self.create_machine(code='Machine1',
                                             serial_number='123456789',
                                             delivery_date='2020-01-01')

        self.assertTrue(isinstance(sample_machine, Machine))
        self.assertEqual('Machine1', sample_machine.code, 'the codes are not the same!')
        self.assertEqual('123456789', sample_machine.serial_number, 'The numbers are not the same!')
        self.assertEqual('2020-01-01', sample_machine.delivery_date, 'the dates are not the same!')
        self.assertEqual(str(sample_machine), sample_machine.code)


class SerialNumberShipmentToCustomerTest(TestCase):

    def setUp(self):
        Customer.objects.create(name='Customer1')
        Machine.objects.create(code='Machine1',
                               serial_number='123456789')

    def create_shipment_to_customer(self, delivery_note_number, customer_name, serial_number):
        return ShipmentToCustomer.objects.create(delivery_note_number=delivery_note_number,
                                                 customer=Customer.objects.get(name=customer_name),
                                                 item=Machine.objects.get(serial_number=serial_number))

    def test_correct_shipment_creation(self):
        today = datetime.now()
        sample_shipment = self.create_shipment_to_customer(delivery_note_number='WZ/01/01/2020',
                                                           customer_name='Customer1',
                                                           serial_number='123456789')
        self.assertTrue(isinstance(sample_shipment, ShipmentToCustomer))
        self.assertEqual('WZ/01/01/2020', sample_shipment.delivery_note_number, 'The numbers are not the same!')
        self.assertEqual('Customer1', sample_shipment.customer.name, 'The customers name are not the same!')
        self.assertEqual('Machine1', sample_shipment.item.code, 'The machines name are not the same!')
        self.assertEqual(today.date(), sample_shipment.shipment_date.date(), 'The dates are not the same!')
        self.assertEqual(str(sample_shipment), sample_shipment.delivery_note_number)




