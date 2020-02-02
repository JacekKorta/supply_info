import re
from serial_numbers.models import Machine


def extract_serial_numbers(data):
    # Data filled in by barcode reader has “\r\n’ on the end of each line.
    # Data filled in manually has only ‘\n’ on the end of the line.
    serials = data.replace('\r', '').split('\n')
    return serials


def parse_serials(serials):
    machines = []
    for item in serials:
        # passed data must be a nine digit number
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
            code = code.strip()
            serial_number = serial_number.strip()
        except ValueError:
            continue
        # passed data must be a nine digit number
        if re.match(r"(?<!\d)\d{9}(?!\d)", serial_number):
            machines.append((code, serial_number))
        else:
            continue
    return machines
