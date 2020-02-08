from serial_numbers.models import Machine
from warranty_parts.models import Issues


def save_issues(form_dict):
    customer, machine_sn, part_number, part_name, quantity, issue_description, document_number = form_dict.values()
    try:
        machine = Machine.objects.get(serial_number=machine_sn)
    except Machine.DoesNotExist:
        machine = None
        print(f'nie znaleziono "{machine_sn}"')
    Issues.objects.create(customer=customer,
                          machine=machine,
                          part_number=part_number,
                          quantity=quantity,
                          issue_description=issue_description,
                          doc_number=document_number)