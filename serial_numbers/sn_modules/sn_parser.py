import re
from serial_numbers.models import Customer, Machine, ShipmentToCustomer


def extract_serial_numbers(data):
    serials = data.split('\r\n')
    return serials


def parse_serials(serials):
    machines = []
    for item in serials:
        if re.match('[0-9]{9}', item):
            machine = Machine.objects.filter(serial_number=item).first()
            if machine:
                machines.append(machine.serial_number)
            else:
                m = Machine(
                    code='Unknown',
                    serial_number=item
                )
                m.save()
                machines.append(item)
        else:
            continue
    return machines

