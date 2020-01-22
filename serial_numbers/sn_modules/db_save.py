from serial_numbers.models import Customer, Machine, ShipmentToCustomer


def shipment_record(customer, delivery_note_number, serial_number):
    shipment = ShipmentToCustomer(
        customer=Customer.objects.get(name=customer),
        delivery_note_number=delivery_note_number,
        item=Machine.objects.get(serial_number=serial_number)
    )
    shipment.save()