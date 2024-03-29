import logging

from serial_numbers.models import Customer, Machine, ShipmentToCustomer

logger = logging.getLogger(__name__)


def shipment_record(customer, delivery_note_number, serial_number):
    shipment = ShipmentToCustomer(
        customer=Customer.objects.get(name=customer),
        delivery_note_number=delivery_note_number,
        item=Machine.objects.get(serial_number=serial_number)
    )
    shipment.save()


def save_delivery(serial_number, code, date):
    try:
        machine = Machine.objects.get(serial_number=serial_number)
        logger.info(f'Maszyna o nr seryjnym {machine.serial_number} jest juz w bazie')
    except Machine.DoesNotExist:
        machine = Machine(
            code=code.strip(),
            serial_number=serial_number.strip(),
            delivery_date=date,
        )
        machine.save()

