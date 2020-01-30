import re
from serial_numbers.models import Customer, Machine, ShipmentToCustomer


def extract_serial_numbers(data):
    serials = data.replace('\r', '').split('\n')
    return serials


def parse_serials(serials):
    machines = []
    for item in serials:
        print(item)
        if re.match(r"(?<!\d)\d{9}(?!\d)", item):
            try:
                machine = Machine.objects.get(serial_number=item)
                machines.append(machine.serial_number)
            except Machine.DoesNotExist:
                m = Machine(
                    code='Unknown',
                    serial_number=item
                )
                m.save()
                machines.append(item)
        else:
            continue
    return machines


def extract_data_to_register_machine(data):
    machines = []
    for machine in data.split('\n'):
        try:
            code, serial_number = machine.split(',')
        except ValueError:
            pass
        if re.match(r"(?<!\d)\d{9}(?!\d)", serial_number):
            machines.append((code, serial_number.strip()))
        else:
            continue
    return machines
