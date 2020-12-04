from googletrans import Translator

from serial_numbers.models import Machine
from warranty_parts.models import Comments, Issues


def issues_desc_translate(description):
    translator = Translator()
    try:
        result = translator.translate(description, dest='en', src='pl')
    except:
        result = None

    if result:
        return f'{result.text}  <=== UWAGA: przetłumaczono automatycznie ==='
    else:
        return ''


def save_issues(form_dict):
    customer, machine_sn, _, part_number, part_name, quantity, issue_description, document_number = form_dict.values()
    try:
        machine = Machine.objects.get(serial_number=machine_sn)
    except Machine.DoesNotExist:
        machine = None
    issues_desc_translate(issue_description)
    issue = Issues.objects.create(customer=customer,
                                  machine=machine,
                                  part_number=part_number,
                                  part_name=part_name,
                                  quantity=quantity,
                                  issue_description=issue_description,
                                  eng_issue_description=issues_desc_translate(issue_description),
                                  doc_number=document_number)
    return issue, machine


def save_comment(body, issue_id, username):
    comment = Comments.objects.create(issue=Issues.objects.get(pk=issue_id),
                                      username=username,
                                      body=body)
    return comment
