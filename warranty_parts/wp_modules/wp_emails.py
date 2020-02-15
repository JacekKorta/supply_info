from django.core.mail import send_mail
from public_python.config import EmailConfigData


def send_new_issue_message(issue, machine):
    subject = f'[SERWIS] Nowe Zgłosznie nr {issue.id}'
    body = f'Zgłosznie nr: {issue.id}\n' \
           f'Kod produktu: {issue.part_number}\n' \
           f'Nazwa produktu: {issue.part_name}\n' \
           f'Maszyna: {machine.code}\n' \
           f'Nr seryjny: {machine.serial_number}\n' \
           f'Opis usterki: {issue.issue_description}\n' \
           f'Część została wpisana na: {issue.doc_number}\n'
    send_mail(subject,
              body,
              EmailConfigData.EMAIL_HOST_USER,
              EmailConfigData.TEST_RECIPIENTS, #zmień na SERVICE_RECIPIENTS
              auth_user=EmailConfigData.EMAIL_HOST_USER,
              auth_password=EmailConfigData.EMAIL_HOST_PASSWORD)


def send_new_comment_notification(issue_id, comment):
    subject = f'[SERWIS][KOMENTARZ] do zgłoszenia {issue_id}'
    body = f'Użytkownik: {comment.username} dodał komentarz do zgłoszenia: {issue_id}:\n' \
           f'{comment.body}\n'

    send_mail(subject,
              body,
              EmailConfigData.EMAIL_HOST_USER,
              EmailConfigData.TEST_RECIPIENTS, #zmień na SERVICE_RECIPIENTS  SERVICE_RECIPIENTS
              auth_user=EmailConfigData.EMAIL_HOST_USER,
              auth_password=EmailConfigData.EMAIL_HOST_PASSWORD)


